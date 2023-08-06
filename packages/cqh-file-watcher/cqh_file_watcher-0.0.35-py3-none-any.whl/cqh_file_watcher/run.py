#!/usr/bin/python
# coding:utf-8
from argparse import Action, SUPPRESS
import os
from cqh_file_watcher import __version__
import argparse
from queue import Queue
import re
import json
import sys
import logging


from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY, IN_MOVED_TO, IN_MOVED_FROM
# https://codereview.stackexchange.com/questions/6567/redirecting-subprocesses-output-stdout-and-stderr-to-the-logging-module

from cqh_file_watcher.command_caller import CommandCaller
from cqh_file_watcher import util


class EventHandler(ProcessEvent):
    def __init__(self, logger, command_list, directory):
        super().__init__()
        self.logger = logger
        self.queue = Queue(maxsize=1)
        self.command_callder = CommandCaller(self.queue, logger)
        self.command_list = command_list
        self.directory = directory.rstrip("/")

    def start(self):
        self.logger.info("begin call command_caller")
        self.command_callder.start()

    def stop(self):
        self.queue.put((True, None), True)

    def process_IN_CREATE(self, event):
        self.handle_event(event)

    def process_IN_DELETE(self, event):
        self.handle_event(event)

    def process_IN_MODIFY(self, event):
        self.handle_event(event)

    def process_IN_MOVE(self, event):
        self.handle_event(event)

    def process_IN_MOVED_TO(self, event):
        self.handle_event(event)

    def process_IN_MOVED_FROM(self, event):
        self.handle_event(event)

    def handle_event(self, event):
        send_data_list = []

        def should_execute_cmd(command, relative_path):
            pattern, ignore_pattern = command.get("pattern"), command.get("ignore_pattern")
            if not ignore_pattern:
                ignore_pattern = []
            else:
                if not isinstance(ignore_pattern, (list, tuple)):
                    ignore_pattern = [ignore_pattern]

            def not_in_ignore_patttern(ignore_pattern_list):
                for _ignore_pattern in ignore_pattern_list:
                    _ignore_pattern = re.compile(_ignore_pattern)
                    if _ignore_pattern.match(relative_path):
                        return False
                return True
            if not pattern:
                return not_in_ignore_patttern(ignore_pattern)
            pattern = re.compile(pattern)
            if pattern.match(relative_path):
                return not_in_ignore_patttern(ignore_pattern)

        for command_d in self.command_list:
            pattern = command_d.get("pattern")
            # generated_by_dict_unpack: command_d
            command = command_d["command"]
            directory = command_d.get("directory") or self.directory
            relative_path = event.pathname[len(self.directory) + 1:]
            logger.debug("relative_path:{}".format(relative_path))
            should_execute = should_execute_cmd(command_d, relative_path)
            # if not pattern:
            #     should_execute = True
            # else:
            #     if not pattern.endswith("$"):
            #         pattern += "$"
            #     pattern = re.compile(pattern)
            #     if pattern.match(relative_path):
            #         should_execute = True
            if should_execute:
                # push command data
                queue_data = dict(
                    pattern=pattern,
                    relative_path=relative_path,
                    path=event.path,
                    command=command,
                    directory=directory,
                )
                send_data_list.append(queue_data)

        if send_data_list:
            if self.queue.full():
                logger.debug("queue is full, so does not put it")
            else:

                self.queue.put([False, send_data_list])


_dir = os.path.dirname(
    os.path.abspath(__file__)
)
from cqh_file_watcher.conf import doc
doc_content = doc


logger = logging.getLogger('cqh_file_watcher')
if not logger.handlers:
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                                                  datefmt='%y%m%d %H:%M:%S'))
    logger.addHandler(stream_handler)


class DocAction(Action):

    def __init__(self,
                 option_strings,
                 dest=SUPPRESS,
                 default=SUPPRESS,
                 help=None):
        super(DocAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        # parser.print_help()
        print(self.default)
        parser.exit()


parser = argparse.ArgumentParser('cqh_file_watcher',
                                 description='watch directory changes and run commands',
                                 )

parser.register("action", "doc", DocAction)


level_choices = logging._nameToLevel
level_choices = [e.lower() for e in level_choices]

parser.add_argument("--level", dest='level', type=str, default="info", choices=level_choices)
parser.add_argument("--conf", dest='conf', help="conf path", required=True)
parser.add_argument("--doc", default=doc_content, action='doc')


def main(argv=None):
    if argv is not None:
        convert_args = parser.parse_args(argv)
    else:
        convert_args = parser.parse_args()
    _inner_run(convert_args.level, convert_args.conf)


def _inner_run(level, conf):
    """Simple program that greets NAME for a total of COUNT times."""
    logger.setLevel(getattr(logging, level.upper()))
    if not os.path.exists(conf):
        logger.error("conf not exitst {}".format(conf))
        return
    logger.debug("version:{}".format(__version__))
    content_d = json.loads(open(conf, "r", encoding='utf-8').read())

    current_dir = os.getcwd()
    logger.info("current_dir:{}".format(current_dir))
    env = os.environ.copy()
    env['DIRECTORY'] = current_dir
    logger.debug('env:{}'.format(env))

    content_d['directory'] = util.string_replace(content_d['directory'], env)
    for ele in content_d['command_list']:
        ele['command'] = util.string_replace(ele['command'], env)
    logger.debug("content:{}".format(json.dumps(
        content_d, ensure_ascii=False, indent=2)))
    # generated_by_dict_unpack: content_d
    directory, command_list = content_d["directory"], content_d["command_list"]
    monitor(directory, command_list)


def monitor(path, command_list):
    wm = WatchManager()
    """
    IN_DELETE | IN_CREATE | IN_MODIFY | 监听不到ansible copy的事件？
    试一试 IN_MOVED_TO？
    """
    mask = IN_DELETE | IN_CREATE | IN_MODIFY | IN_MOVED_FROM | IN_MOVED_TO
    handler = EventHandler(logger, command_list=command_list,
                           directory=path)
    notifier = Notifier(wm, handler)
    handler.start()
    wm.add_watch(path, mask, auto_add=True, rec=True)
    logger.info("now start monitor %s" % path)
    while 1:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            handler.stop()
            break


if __name__ == "__main__":
    main()
