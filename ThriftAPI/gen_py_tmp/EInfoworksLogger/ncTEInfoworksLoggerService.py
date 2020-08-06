#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []


class Iface(object):
    def Log_AddLog(self, entry):
        """
        记入 Log 信息
        当日志记录的量超过一定的阈值时，会对日志进行裁切，丢弃最早记录的日志。
        @param entry         日志内容
           该接口不抛出异常!!

        Parameters:
         - entry

        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def Log_AddLog(self, entry):
        """
        记入 Log 信息
        当日志记录的量超过一定的阈值时，会对日志进行裁切，丢弃最早记录的日志。
        @param entry         日志内容
           该接口不抛出异常!!

        Parameters:
         - entry

        """
        self.send_Log_AddLog(entry)

    def send_Log_AddLog(self, entry):
        self._oprot.writeMessageBegin('Log_AddLog', TMessageType.ONEWAY, self._seqid)
        args = Log_AddLog_args()
        args.entry = entry
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["Log_AddLog"] = Processor.process_Log_AddLog
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_Log_AddLog(self, seqid, iprot, oprot):
        args = Log_AddLog_args()
        args.read(iprot)
        iprot.readMessageEnd()
        try:
            self._handler.Log_AddLog(args.entry)
        except TTransport.TTransportException:
            raise
        except Exception:
            logging.exception('Exception in oneway handler')

# HELPER FUNCTIONS AND STRUCTURES


class Log_AddLog_args(object):
    """
    Attributes:
     - entry

    """


    def __init__(self, entry=None,):
        self.entry = entry

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.entry = ncTLogItem()
                    self.entry.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('Log_AddLog_args')
        if self.entry is not None:
            oprot.writeFieldBegin('entry', TType.STRUCT, 1)
            self.entry.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(Log_AddLog_args)
Log_AddLog_args.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'entry', [ncTLogItem, None], None, ),  # 1
)
fix_spec(all_structs)
del all_structs

