#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:58:27 2019

@author: timepi

@description: this is a tool to do statistic for functions
"""
import json
import toml
import time
import socket
import logging
import traceback
from enum import IntEnum
from functools import wraps
from threading import Thread
from collections import namedtuple
from prometheus_client import Gauge
from queue import Queue, Empty, Full
from prometheus_client import push_to_gateway
from prometheus_client import CollectorRegistry

# define status summary namedtuple
StatusSummary = namedtuple('StatusSummary', 'total counter_total max_cost cost_total')

# global singleton object
GlobalPrometheusStatusImpl = None


class StatusCode(IntEnum):
    OK = 0
    ERR = 1


class StatusItem:
    def __init__(self, name):
        self.name, self.status, self.counter, self.time_diff = name, StatusCode.OK, 0, time.time()

    def set_counter(self, counter):
        self.counter = counter

    def mark_ok(self):
        self.status = StatusCode.OK

    def mark_err(self):
        self.status = StatusCode.ERR

    def end(self):
        self.time_diff = time.time() - self.time_diff


class PrometheusStatusExporter(Thread):
    buffer_size = 20000
    max_time_gap = 30

    @staticmethod
    def get_host():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect('8.8.8.8', 80)
            s.close()
            return s.getpeername()[0]
        finally:
            return 'unknown'

    def __init__(self, config_file=None):
        Thread.__init__(self, name='PrometheusStatusExporter', daemon=True)
        if config_file is not None:
            self.config = toml.load(config_file)
            self.url = self.config['prome']['host']
            self.prome_status = self.config['prome']['status']
            self.job = self.config['server']['name']
            self.log_file = self.config['server']['log_file']
        else:
            self.url = ''
            self.prome_status = False
            self.job = 'PrometheusStatusExporter'
            self.log_file = '/tmp/prometheus_status_export.log'

        self.host = PrometheusStatusExporter.get_host()
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='[%Y-%m-%d %H:%M:%S]',
            filename=self.log_file,
            filemode='a'
        )
        self.summary_cache = {}
        self.status_queue = Queue(PrometheusStatusExporter.buffer_size)

    def add(self, status_item):
        try:
            self.status_queue.put(status_item, block=False)
        except Full:
            logging.info('status item queue is full')
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def push(self, kv, labels):
        if not self.prome_status:
            logging.info('%s %s' % (json.dumps(labels), json.dumps(kv)))
            return
        try:
            reg = CollectorRegistry()
            labels['host'] = self.host
            for name, value in kv.items():
                g = Gauge(name, '', labels.keys(), registry=reg)
                g.labels(**labels).set(value)
            push_to_gateway(self.url, job=self.job, timeout=3, registry=reg)
        except:
            traceback.print_exc()
            logging.error(traceback.format_exc())

    def summary(self, status_items):
        for status_item in status_items:
            try:
                if status_item.name not in self.summary_cache:
                    self.summary_cache[status_item.name] = {}
                if status_item.status not in self.summary_cache[status_item.name]:
                    s = StatusSummary(1, status_item.counter, status_item.time_diff, status_item.time_diff)
                    self.summary_cache[status_item.name][status_item.status] = s
                else:
                    old_s = self.summary_cache[status_item.name][status_item.status]
                    new_s = StatusSummary(1 + old_s.total, old_s.counter_total + status_item.counter,
                                          max(status_item.time_diff, old_s.max_cost),
                                          old_s.cost_total + status_item.time_diff)
                    self.summary_cache[status_item.name][status_item.status] = new_s
            except:
                traceback.print_exc()
                logging.error(traceback.format_exc())

    def export(self):
        for name, status_value in self.summary_cache.items():
            for status, summary in status_value.items():
                if summary.total <= 0 or summary.cost_total <= 0:
                    continue
                kvs = {'%s_total' % name: summary.total, '%s_qps' % name: summary.total / summary.cost_total,
                       '%s_counter' % name: summary.counter_total,
                       '%s_avg_counter' % name: summary.counter_total / summary.total,
                       '%s_max_cost' % name: summary.max_cost
                       }
                self.push(kvs, {'status': 'OK' if status.value == 0 else 'ERR'})
        self.summary_cache = {}

    def collect(self):
        now, max_time = time.time(), time.time() + PrometheusStatusExporter.max_time_gap
        items = []
        while now <= max_time:
            try:
                item = self.status_queue.get(block=False)
                items.append(item)
            except Empty:
                logging.info('status item queue is empty')
                break
            except:
                traceback.print_exc()
                logging.error(traceback.format_exc())
                break
            finally:
                now = time.time()

        if len(items) > 0:
            self.summary(items)
        if len(self.summary_cache) > 0:
            self.export()

    def run(self):
        while 1:
            try:
                start_time = time.time()
                self.collect()
                end_time = time.time()
                diff = end_time - start_time
                if diff < PrometheusStatusExporter.max_time_gap:
                    time.sleep(PrometheusStatusExporter.max_time_gap - diff)
            except:
                traceback.print_exc()
                logging.error(traceback.format_exc())
                time.sleep(1)


def init(config_file=None):
    global GlobalPrometheusStatusImpl
    if GlobalPrometheusStatusImpl is None:
        GlobalPrometheusStatusImpl = PrometheusStatusExporter(config_file)
        GlobalPrometheusStatusImpl.start()


def export(func):
    @wraps(func)
    def wrapper(*argv, **kwargs):
        global GlobalPrometheusStatusImpl
        stat = StatusItem(func.__name__)
        ret = func(*argv, **kwargs)
        stat.mark_ok()
        stat.end()
        GlobalPrometheusStatusImpl.add(stat)
        return ret

    return wrapper
