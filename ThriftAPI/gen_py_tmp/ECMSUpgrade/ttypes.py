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
import EThriftException.ttypes

from thrift.transport import TTransport
all_structs = []


class ncTUpgradePackageInfo(object):
    """
    升级包信息

    Attributes:
     - package_version
     - support_version
     - import_time
     - package_hash
     - hash_algorithm
     - package_name
     - package_size

    """


    def __init__(self, package_version="", support_version="", import_time=0, package_hash="", hash_algorithm="", package_name="", package_size=0,):
        self.package_version = package_version
        self.support_version = support_version
        self.import_time = import_time
        self.package_hash = package_hash
        self.hash_algorithm = hash_algorithm
        self.package_name = package_name
        self.package_size = package_size

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
                if ftype == TType.STRING:
                    self.package_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.support_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.import_time = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.package_hash = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.hash_algorithm = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.package_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I64:
                    self.package_size = iprot.readI64()
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
        oprot.writeStructBegin('ncTUpgradePackageInfo')
        if self.package_version is not None:
            oprot.writeFieldBegin('package_version', TType.STRING, 1)
            oprot.writeString(self.package_version.encode('utf-8') if sys.version_info[0] == 2 else self.package_version)
            oprot.writeFieldEnd()
        if self.support_version is not None:
            oprot.writeFieldBegin('support_version', TType.STRING, 2)
            oprot.writeString(self.support_version.encode('utf-8') if sys.version_info[0] == 2 else self.support_version)
            oprot.writeFieldEnd()
        if self.import_time is not None:
            oprot.writeFieldBegin('import_time', TType.I64, 3)
            oprot.writeI64(self.import_time)
            oprot.writeFieldEnd()
        if self.package_hash is not None:
            oprot.writeFieldBegin('package_hash', TType.STRING, 4)
            oprot.writeString(self.package_hash.encode('utf-8') if sys.version_info[0] == 2 else self.package_hash)
            oprot.writeFieldEnd()
        if self.hash_algorithm is not None:
            oprot.writeFieldBegin('hash_algorithm', TType.STRING, 5)
            oprot.writeString(self.hash_algorithm.encode('utf-8') if sys.version_info[0] == 2 else self.hash_algorithm)
            oprot.writeFieldEnd()
        if self.package_name is not None:
            oprot.writeFieldBegin('package_name', TType.STRING, 6)
            oprot.writeString(self.package_name.encode('utf-8') if sys.version_info[0] == 2 else self.package_name)
            oprot.writeFieldEnd()
        if self.package_size is not None:
            oprot.writeFieldBegin('package_size', TType.I64, 7)
            oprot.writeI64(self.package_size)
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


class ncTNodeUpgradeStatus(object):
    """
    节点升级状态

    Attributes:
     - node_uuid
     - status
     - comment
     - errors
     - last_time
     - start_time
     - old_version
     - new_version

    """


    def __init__(self, node_uuid="", status="", comment="", errors=[
    ], last_time=0, start_time=0, old_version="", new_version="",):
        self.node_uuid = node_uuid
        self.status = status
        self.comment = comment
        if errors is self.thrift_spec[4][4]:
            errors = [
            ]
        self.errors = errors
        self.last_time = last_time
        self.start_time = start_time
        self.old_version = old_version
        self.new_version = new_version

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
                if ftype == TType.STRING:
                    self.node_uuid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.status = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.comment = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.errors = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.errors.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I64:
                    self.last_time = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I64:
                    self.start_time = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.STRING:
                    self.old_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.STRING:
                    self.new_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('ncTNodeUpgradeStatus')
        if self.node_uuid is not None:
            oprot.writeFieldBegin('node_uuid', TType.STRING, 1)
            oprot.writeString(self.node_uuid.encode('utf-8') if sys.version_info[0] == 2 else self.node_uuid)
            oprot.writeFieldEnd()
        if self.status is not None:
            oprot.writeFieldBegin('status', TType.STRING, 2)
            oprot.writeString(self.status.encode('utf-8') if sys.version_info[0] == 2 else self.status)
            oprot.writeFieldEnd()
        if self.comment is not None:
            oprot.writeFieldBegin('comment', TType.STRING, 3)
            oprot.writeString(self.comment.encode('utf-8') if sys.version_info[0] == 2 else self.comment)
            oprot.writeFieldEnd()
        if self.errors is not None:
            oprot.writeFieldBegin('errors', TType.LIST, 4)
            oprot.writeListBegin(TType.STRING, len(self.errors))
            for iter6 in self.errors:
                oprot.writeString(iter6.encode('utf-8') if sys.version_info[0] == 2 else iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.last_time is not None:
            oprot.writeFieldBegin('last_time', TType.I64, 5)
            oprot.writeI64(self.last_time)
            oprot.writeFieldEnd()
        if self.start_time is not None:
            oprot.writeFieldBegin('start_time', TType.I64, 6)
            oprot.writeI64(self.start_time)
            oprot.writeFieldEnd()
        if self.old_version is not None:
            oprot.writeFieldBegin('old_version', TType.STRING, 7)
            oprot.writeString(self.old_version.encode('utf-8') if sys.version_info[0] == 2 else self.old_version)
            oprot.writeFieldEnd()
        if self.new_version is not None:
            oprot.writeFieldBegin('new_version', TType.STRING, 8)
            oprot.writeString(self.new_version.encode('utf-8') if sys.version_info[0] == 2 else self.new_version)
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
all_structs.append(ncTUpgradePackageInfo)
ncTUpgradePackageInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'package_version', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'support_version', 'UTF8', "", ),  # 2
    (3, TType.I64, 'import_time', None, 0, ),  # 3
    (4, TType.STRING, 'package_hash', 'UTF8', "", ),  # 4
    (5, TType.STRING, 'hash_algorithm', 'UTF8', "", ),  # 5
    (6, TType.STRING, 'package_name', 'UTF8', "", ),  # 6
    (7, TType.I64, 'package_size', None, 0, ),  # 7
)
all_structs.append(ncTNodeUpgradeStatus)
ncTNodeUpgradeStatus.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'node_uuid', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'status', 'UTF8', "", ),  # 2
    (3, TType.STRING, 'comment', 'UTF8', "", ),  # 3
    (4, TType.LIST, 'errors', (TType.STRING, 'UTF8', False), [
    ], ),  # 4
    (5, TType.I64, 'last_time', None, 0, ),  # 5
    (6, TType.I64, 'start_time', None, 0, ),  # 6
    (7, TType.STRING, 'old_version', 'UTF8', "", ),  # 7
    (8, TType.STRING, 'new_version', 'UTF8', "", ),  # 8
)
fix_spec(all_structs)
del all_structs
