/*********************************************************************************

ERomote.thrift:
    ���� AT����Զ�̽ӿڶ����ļ�	
    Copyright (c) Eisoo Software, Inc.(2012 - ), All rights reserved.

Purpose:
    �˽ӿ��ļ����� AT����Զ�̽ӿڡ�

Author:
    zhong.hua(zhong.hua@eisoo.cn)
	
Creating Time:
    2012-12-5
    
*********************************************************************************/

include "EThriftException.thrift"

typedef i32 int32
typedef i64 int64

const int32 NCT_ERomote_PORT = 9091

typedef list<string> ncRemoteList
typedef list<string> ncTransferList

service ncTERemote {

	/**
	 *
	 * ִ�пͻ����͹���������
	 *
	 * @throw EThriftException.ncTException: 1.��ȡʧ��
	 *
	 *
	 */
	 void run_commands(1: ncRemoteList commandline)
	              throws (1: EThriftException.ncTException exp)
				  
	 void run_commands_return(1: ncRemoteList commandline)
	              throws (1: EThriftException.ncTException exp)
	 
	 void Transfer(1: ncTransferList file,2: string ip,3: int32 port )
	              throws (1:EThriftException.ncTException exp) 
}