/*******************************************************************************************
EVFS.thrift
    Copyright (c) Eisoo Software, Inc.(2013 - 2014), All rights reserved

Purpose:
        EVFS 数据管理接口.
        提供 GNS 管理对象的增删查等.

Author:
    Liu Lang (liu.lang@eisoo.cn)

Creating Time:
    2013-05-13
*******************************************************************************************/

include "EThriftException.thrift"

/**
 * 端口号
 */
const i32 NCT_EVFS_PORT = 9064

/**
 * 自定义的时间类型
 */
struct ncTEVFSDate {
    1: required i32 year = 1970,
    2: required i32 month = 1,
    3: required i32 day = 1,
    4: required i32 hour = 0,
    5: required i32 min = 0,
    6: required i32 sec = 0,
}

/**
 * GNS 对象
 */
struct ncTEVFSGNSObject {
    1: required string gns,                           // GNS 路径
    2: required string name,                          // 名字
}

/**
 * GNS 对象集
 */
struct ncTEVFSGNSObjectSet {
    1: required list<ncTEVFSGNSObject> gnsObjects,    // GNS 对象集
}

/**
 * 文件统计-统计日期单位
 */
enum ncTEVFSDateUnit {
    NCT_EVFS_DATE_YEAR = 1,
    NCT_EVFS_DATE_MONTH = 2,
    NCT_EVFS_DATE_DAY = 3,
}

/**
 * 文件统计-标识文件数量的结构体
 */
struct ncTEVFSFilesCount {
    1: required i64 docNum,            // 文档数量
    2: required i64 picNum,            // 图片数量
    3: required i64 vidNum,            // 视频数量
    4: required i64 othNum,            // 其它文件数量
    5: required i64 total,             // 总数
}

/**
 * 文件统计-标识文件变化趋势的结构体
 */
struct ncTEVFSFilesChanged {
    1: required ncTEVFSFilesCount createOp,            // 文件增加操作
    2: required ncTEVFSFilesCount modifyOp,            // 文件更新操作
    3: required ncTEVFSFilesCount deleteOp,            // 文件删除操作
}

/**
 * 配额空间中的信息
 */
struct ncTEVFSQuotaInfo {
    1: required i64 quota,        // 配额空间的大小(单位:Byte)
    2: required i64 usedsize,     // 已经使用空间的大小(单位:Byte)
}

/**
 * 资源对象信息
 */
struct ncTETSResourceInfo {
    1: required string otag,     // 资源对象标记
    2: required i64 size,        // 资源对象大小，-1表示为文件夹
}

struct ncTResourceInfo {
    1: required string gns,      // 资源对象GNS路径
    2: required string otag,     // 资源对象标记
    3: required i64 size,        // 资源对象大小，初始值-2，-1为目录，>=0为文件
    4: required i64 modified,    // 最近修改时间：client_mtime不为0，则取client_mtime，否则取time
}

/**
 * 操作统计中的操作类型
 */
enum ncTEVFSOperatedType {
    NCT_EVFS_OP_UNKNOWN                = 0,         // 未知
    NCT_EVFS_OP_DIR_CREATED            = 1,         // 目录创建
    NCT_EVFS_OP_DIR_DEL_TO_RECYCLE     = 2,         // 目录删除至回收站
    NCT_EVFS_OP_DIR_LIST               = 3,         // 目录浏览
    NCT_EVFS_OP_DIR_RENAME             = 4,         // 目录重命名
    NCT_EVFS_OP_DIR_RESOTRE            = 5,         // 目录从回收站还原
    NCT_EVFS_OP_DIR_DELETE             = 6,         // 目录从回收站彻底删除
    NCT_EVFS_OP_DIR_MOVE               = 7,         // 目录移动
    NCT_EVFS_OP_DIR_COPY               = 8,         // 目录拷贝
    NCT_EVFS_OP_FILE_CREATED           = 11,        // 文件创建（首次上传）
    NCT_EVFS_OP_FILE_MODIFY            = 12,        // 文件编辑
    NCT_EVFS_OP_FILE_DEL_TO_RECYCLE    = 13,        // 文件删除至回收站
    NCT_EVFS_OP_FILE_DOWNLOAD          = 14,        // 文件下载
    NCT_EVFS_OP_FILE_RAPID_SUCCEE      = 15,        // 秒传成功
    NCT_EVFS_OP_FILE_RAPID_FAIL        = 16,        // 秒传失败
    NCT_EVFS_OP_FILE_RENAME            = 17,        // 文件重命名
    NCT_EVFS_OP_FILE_RESTORE           = 18,        // 文件从回收站还原
    NCT_EVFS_OP_FILE_DELETE            = 19,        // 文件从回收站彻底删除
    NCT_EVFS_OP_FILE_COPY              = 20,        // 文件拷贝
    NCT_EVFS_OP_FILE_MOVE              = 21,        // 文件移动
}

/**
 * 秒传统计信息
 */
struct ncTEVFSRapidStatisInfo {
    1: required i64         fileCount,             // 文件数量
    2: required i64         rapidCount,            // 秒传次数
    3: required i64         saveTotal,             // 节省总空间 (字节)
}

/**
 * 秒传文件信息
 */
struct ncTEVFSRapidFileInfo {
    1: required string             verDataId;       // 版本数据ID
    2: required string             name,            // 文件名
    3: required i64                date,            // 时间戳(精确到毫秒)
    4: required i32                refCount,        // 引用数
    5: required i64                fileSize,        // 文件大小 (字节)
    6: required i64                saveSize,        // 节省空间 (字节)
}

/**
 * 内存缓存统计
 */
struct ncTEVFSListCacheInfo {
    1: required i64 listNum,               // 列举次数
    2: required i64 hitNum,                // 命中次数
}

/**
 * 向开放存储的请求信息
 */
struct ncTEVFSOSSRequest {
    1: string method;           // 请求的方法
    2: string url;
    3: list<string> headers;    // headers 可能为空
    4: string body;             // PUT 请求的内容，只用于返回完成分块上传的body信息
}

/**
 * 向开放存储上传的分块信息
 */
struct ncTEVFSOSSPartInfo {
    1: required string etag,     // 分块标识
    2: required i64 size,        // 分块大小
}

/**
 * 站点类型
 */
enum ncTEVFSSiteType {
    NCT_SITE_TYPE_NORMAL = 0,    // 普通站点类型
    NCT_SITE_TYPE_MASTER = 1,    // 主站点类型
    NCT_SITE_TYPE_SLAVE = 2,     // 从站点类型
}

/**
 * 站点信息
 */
struct ncTEVFSSiteEossInfo {
    1: required string ip,              // 站点ip/域名
    2: required i32 eossHTTPPort,       // EOSS 对象数据服务端口
    3: required i32 eossHTTPSPort,      // EOSS 对象数据服务安全端口
    4: required ncTEVFSSiteType type,   // 站点类型
    5: required string name,            // 站点名称
    6: required i32 status,             // 站点状态：0表示禁用，1表示可用
    7: required string eossIp,          // 存储ip
}

/*
 * 支持的对象存储服务
 * ASU   : AnyShare Universal
 * CEPH  : Ceph
 * OSS   : 阿里云
 * BOS   : 百度开放云
 * QINIU : 七牛云存储
 * AWS   : 亚马逊
 * AWSCN : 亚马逊中国
 * AZURE : 微软Azure
 * SEOSS : 单个 EOSS
 * HCPS3 : 日立
 * UCLOUD: UCLOUD UFile对象存储
 */

/*
 * 对象存储URL中，bucket使用的访问方式，path-style或bucket virtual hosting */
enum ncTEVFSOSSBucketStyle {
    NCT_PATH_STYLE = 0,
    NCT_VIRTUAL_HOSTING_STYLE = 1,
}

/**
 * 对象存储服务信息
 */
struct ncTEVFSOSSInfo {
    1: required string provider,            // 服务提供商
    2: string accessId,                     // 使用对象存储的账户id
    3: string accessKey,                    // 使用对象存储的账户key
    4: string bucket,
    5: required string serverName,          // 服务器地址
    6: i32 httpsPort,                       // 服务器https端口
    7: i32 httpPort,                        // 服务器http端口
    8: string internalServerName,           // 内部服务器地址
    9: string cdnName,                      // CDN 加速域名
    10: i32 type,                           // 0 表示为了兼容性保存的已启用存储，1 表示可选的新存储
    11: string ossId,                       // 该对象存储的标识id，留作内部使用
    12: string providerDetail,              // 服务提供商的详细信息，用于区分不同的细分厂商或产品名
    13: ncTEVFSOSSBucketStyle bucketStyle,  // URL中，bucket使用path-style或bucket virtual hosting访问方式
}

/**
 * 大文件传输限制时，排除掉的网段
 */
struct ncTEVFSNetworkSegment {
    1: required string ip,
    2: required string netMask,             // 网络掩码
}

/**
 * 大文件传输限制：上传还是下载
 */
enum ncTEVFSTransferOption {
    NCT_UPLOAD = 1,                             // 限制上传
    NCT_UPLOAD_AND_DOWNLOAD = 2,                // 限制上传和下载
}

/**
 * 大文件传输限制配置信息
 */
struct ncTEVFSLargeFileLimitConf {
    1: required bool enabled,               // 是否启用大文件传输限制
    2: required i64 size,                   // 限制的文件大小
    3: required list<ncTEVFSNetworkSegment> networkSegment, // 不限制的网段
    4: required ncTEVFSTransferOption option,    // 限制选项
}

/**
 * 限制上传的文件类型
 */
enum ncTSuffixType {
    NCT_DOCS = 1,                   // 文档类文件
    NCT_VIDEOS = 2,                 // 音视频类文件，
    NCT_IMAGES = 3,                 // 图片类文件
    NCT_COMPRESSION = 4,            // 压缩类
    NCT_SUSPICION = 5,              // 可疑类
    NCT_VIRUSES = 6,                // 病毒类
    NCT_OTHERS = 7,                 // 其他文件
}

/**
 * 限制上传的配置信息
 */
struct ncTLimitSuffixDoc {
    1: ncTSuffixType suffixType;       // 后缀类型名
    2: string suffixes;                // 具体后缀
    3: bool denyFlag;                  // 拒绝标识
}

/**
 * 自定义属性类型
 */
enum ncTEVFSCustomAttributeType {
    NCT_ATTRIBUTE_TYPE_LEVEL = 0,              // 层级
    NCT_ATTRIBUTE_TYPE_ENUM = 1,               // 枚举
    NCT_ATTRIBUTE_TYPE_NUMBER = 2,             // 数字
    NCT_ATTRIBUTE_TYPE_TEXT = 3,               // 文本
    NCT_ATTRIBUTE_TYPE_TIME = 4,               // 时间 （单位秒）
}

/**
 * 用户自定义属性信息
 */
struct ncTEVFSCustomAttribute {
    1: i64 id;                                                   // 唯一id
    2: required string name;                                     // 属性名称
    3: required ncTEVFSCustomAttributeType type;                 // 属性类型
    4: required bool searchable;                                 // 是否可被检索
    5: required i32 order;                                       // 显示顺序
    6: i32 status;                                               // 状态 0：隐藏 1：显示
    7: string values;                                            // 属性值 JSON值
                                                                 // JSON定义：  [{"name": "asd", "child": [{"name": "asd1"}] }]
}

/**
 * 需保存对象元数据的应用信息
 */
struct ncTEVFSObjMetaAppInfo {
    1: required string name;            // 应用名
    2: required i32 status,             // 应用状态：0表示禁用，1表示启用
}

/**
 * 站点使用的存储信息
 */
struct ncTEVFSSiteOSS {
    1: required string masterOSS;   // 主存储
    2: required string syncToOSS;   // 备份/同步使用的存储
    3: required i32 roleStatue;     // 主备存储角色互换  1: 不互换 2: 互换主备
    4: required i32 syncMode;       // 同步模式 0: 不同步 1: 单向同步 2: 双向同步
}


/**
 * 数据自备份配置信息
 */
struct ncTEVFSDataSelfBackupConfig {
    1: required bool enable;             // 是否启用数据自备份
    2: required bool enable_sync_delete; // 是否启用数据同步删除，默认不启用
    3: required i32 startHour;           // 开始时间，有效值为 [0,23] 和 -1，-1表示不限制备份时间
    4: required i32 endHour;             // 结束时间，有效值为 [0,23]
}


// 用户文档下载限制信息
struct ncTUserDownloadLimitInfo
{
    1: required string userId;      // 用户名
    2: required i64 limitValue;     // 最大允许的单日下载量
}


/**
 * 隔离区隔离类型
 */
enum ncTEVFSQuarantineType {
    NCT_EVFS_ILLEGAL = 1,
    NCT_EVFS_VIRUS = 2,
    NCT_EVFS_KEY_WORD = 4,
}

// 隔离区申诉信息
struct ncTAppealInfo {
    1: required bool needReview;
    2: required string appellant;
    3: required string appealReason;
}

/**
 * 非法隔离区文件信息
 */
struct ncTEVFSQuarantineFileInfo {
    1: required string docid;
    2: required string versionId;
    3: required string name;
    4: required string modifier;
    5: required i64 modifie_time;
    6: required string parentPath;
    7: required ncTEVFSQuarantineType type;
    8: required string reason;
    9: required i64 serverTime;
    10: required i64 appealExpiredTime;
    11: required ncTAppealInfo appeal;
    12: required i64 quarantineTime;
    13: required string creator;
}

// 控制台隔离区相关设置参数
struct ncTQuarantineConfig {
    1: required i32 appealProtectTime;
    2: required i32 autoDeleteTime;
    3: required bool autoDeleteEnable;
}

// 隔离接口返回参数、用于记日志
struct ncTQuarantineRetMsg {
    1: required string fileName;
    2: required string versionName;
    3: required string parentPath;
}

// 隔离区记录状态（用于获取隔离区列表时过滤）
enum ncTQuarantineState {
    NCT_EVFS_ALL = 1,
    NCT_EVFS_APPEAL = 2,
}

// 获取隔离区列表过滤参数
struct ncTFiltrationParam {
    1: required string key;
    2: required ncTQuarantineState appeal;
    3: required ncTEVFSQuarantineType type;
    4: optional i32 quarantineType;
}

// 下载文件返回信息
struct ncTOSDowndloadRetParam {
    1: required string rev;
    2: required string name;
    3: required string editor;
    4: required i64 modified;
    5: required i64 size;
    6: required i64 client_mtime;
    7: required list<string> auth_request;
    8: required bool need_watermark;
}

/**
 * 外链文件信息
 */
struct ncTEVFSOutLinkFileInfo {
    1: required string creator;     // 文件创建者
    2: required string editor;      // 文件版本编辑者
    3: required i64 modified;       // 文件版本时间
    4: required string sharer;      // 文件共享者
    5: required string sharedObj;   // 共享对象名
}


/**
 * 外链访问信息
 */
struct ncTEVFSOutLinkAccessInfo {
    1: required i64    id;               // 记录id
    2: required string rev;              // 文件版本ID
    3: required string fileName;         // 文件名
    4: required string filePath;         // 文件路径
    5: required string ip;               // 访问ip
    6: required i64    date;             // 访问时间
    7: required i32    opType;           // 操作类型
    8: required string gns;              // 留底文件gns
}

/**
 * 外链访问信息总数
 */
struct ncTEVFSOutLinkAccessInfoCount {
    1: i64 count;           // 数量
    2: i64 maxId;           // 最大的记录Id
}

/**
 * 分页获取外链访问信息参数
 * start：起始号，>= 0
 * limit：取的条数，与start实现分页，-1表示不限制，其它负数值非法
 *      例如[0,-1]表示取所有的
 *      [0, 5] 表示取前5条
 *      [5, -1] 表示从第5条开始，后面所有的
 */
struct ncTEVFSGetPageOutLinkAccessInfoParam {
    1: string name;            // 文件名，模糊匹配
    2: i64 maxId;              // 最大的记录Id
    3: i32 start;              // 开始号
    4: i32 limit;              // 条数
}

/**
 * 文件元数据
 */
struct ncTEVFSFileMetadata {
    1: required string rev;    // 文件版本ID
    2: required string name;   // 文件版本上传时文件名
    3: required string editor; // 文件版本上传编辑者名称
    4: required i64 modified;  // 文件版本上传时间，UTC时间
}

/**
 * 文件属性
 */
struct ncTEVFSFileAttribute {
    1: required string creator; // 文件创建者
    2: required i64 createTime; // 文件创建时间
    3: required i32 csfLevel;   // 文件密级
    4: required string name;    // 文件名
}

/**
 * 文件和最新元数据信息
 */
struct ncTEVFSFileInfo {
    1: required string docId;                   // 文件gns路径
    2: required string path;                    // 文件父路径
    3: required bool retained;                  // 是否为留底的文件
    4: required ncTEVFSFileAttribute attribute; // 文件属性
    5: required ncTEVFSFileMetadata metadata;   // 最新元数据
}

/**
 * 文件信息总数
 */
struct ncTEVFSFileInfoCount {
    1: i64 count;              // 数量
    2: i64 maxCreateTime;      // 最大的createTime
}

/**
 * 分页获取文件信息参数
 * start：起始号，>= 0
 * limit：取的条数，与start实现分页，-1表示不限制，其它负数值非法
 *      例如[0,-1]表示取所有的
 *      [0, 5] 表示取前5条
 *      [5, -1] 表示从第5条开始，后面所有的
 */
struct ncTEVFSGetPageFileInfoParam {
    1: string name;            // 文件名，模糊匹配
    2: i64 maxCreateTime;      // 最大的createTime
    3: i32 start;              // 开始号
    4: i32 limit;              // 条数
}

// 错误码
const string NCT_EVFS_ERR_PROVIDER_NAME = "evfstimpl"
enum ncTEVFSError {
    NCT_INVALID_NULL_ARGUMENT = 10001,                          // 参数错误
    NCT_FAILED_TO_GET_EOFS_MGR = 10002,                         // 获取ncIEOFSManager对象失败
    NCT_FAILED_TO_GET_EVFS = 10003,                             // 获取ncIEVFS对象失败
    NCT_FAILED_TO_GET_EVFS_OTAG_IOC = 10004,                    // 获取ncIEVFSOTagIOC对象失败
    NCT_ONLY_SUPPORT_GNS_CID_OBJECT = 10005,                    // 当前操作仅支持GNS的CID对象
    NCT_FAILED_TO_SET_VERSION_MAX_NUM = 10006,                  // 设置历史版本保留数错误，必须为大于0，小于等于64的整数
    NCT_FAILED_TO_SET_VERSION_BUILD_CYCLE = 10007,              // 设置版本生成周期错误，必须为大于0，小于等于60的整数
    NCT_FAILED_TO_GET_MEM_FILE_RECORD_MGR = 10008,              // 创建内存记录管理器失败
    NCT_INVALID_PARAM_DATA = 10009,                             // 时间参数错误
    NCT_FAILED_TO_GET_EVFS_SPACE_QUOTA = 10010,                 // 创建ncIEVFSQuotaSpaceIOC对象失败
    NCT_INVALID_SPACE_QUOTA = 10011,                            // 空间配额信息出错
    NCT_FAILED_TO_GET_ETS_RESOURECE_INFO = 10012,               // 获取ETS资源信息错误
    NCT_FAILED_TO_CREATE_STATIS_IOC = 10013,                    // 创建ncEVFSStatisticsIOC对象失败
    NCT_FAILED_TO_CREATE_FINGERPRINT_IOC = 10014,               // 创建ncEVFSFingerprintIOC对象失败
    NCT_INVALID_TEVFSOP_TYPE_ARGUMENT = 10015,                  // 无效的TEVFS操作类型参数
    NCT_INVALID_TEVFSDATE_ARGUMENT = 10016,                     // 无效的TEVFS时间类型
    NCT_INVALID_RAPID_FILE_COUNT_OVERSIZE = 10017,              // 秒传信息统计查询数据量不能大于500
    NCT_FAILED_TO_GET_RECYCLE_OBJECT = 10018,                   // 获取回收站对象失败
    NCT_SPACE_QUOTA_NOT_ENOUGH = 10019,                         // 配额空间不足
    NCT_CAN_ONLY_GET_FILE_CSFLEVEL = 10020,                     // 只能获取文件的密级
    NCT_CAN_NOT_CREATE_DIR_UNDER_CURRENT_OBJ = 10021,           // 不能在该类型对象下创建目录
    NCT_SAME_NAME_OBJECT_EXIST = 10022,                         // 存在同名对象
    NCT_SAME_NAME_OBJECT_NOT_UNIQUE = 10023,                    // 名字代表的对象不唯一
    NCT_INTERNAL_ERROR = 10024,                                 // 内部错误
    NCT_CAN_NOT_CHANGE_TP_OSS_PROVIDER = 10025,                 // 不能更换第三方对象存储的服务商
    NCT_UNSUPPORTED_TP_OSS_PROVIDER = 10026,                    // 不支持的第三方对象存储服务
    NCT_CALL_NODE_UPDATE_INTERFACE_ERROR = 10027,               // 调用节点更新接口失败
    NCT_NOT_SUPPORT_GNS_CID_OBJECT = 10028,                     // 不支持操作CID对象
    NCT_USER_CSFLEVEL_LOWER_THAN_DOC = 10029,                   // 用户密级低于给定对象（子对象）
    NCT_FAILED_TO_CREATE_CUSTOM_ATTR_IOC = 10030,               // 创建ncEVFSCustomAttrIOC对象失败
    NCT_INVALID_CUSTOM_ATTR_NAME = 10031,                       // 文件属性名无效
    NCT_CUSTOM_ATTR_ERR_EXCEED_MAX_LEVEL = 10032,               // 属性值层级过多
    NCT_CUSTOM_ATTR_ERR_DUPLICATE_NAME =10033,                  // 名称重复
    NCT_CUSTOM_ATTR_ERR_EXCEED_MAX_ATTR =10034,                 // 属性值超过20个
    NCT_FAILED_TO_CREATE_OBJMETADATA_DBMGR_IOC = 10035,         // 创建 ncIEVFSObjMetadataDBMgr 对象失败
    NCT_FAILED_TO_CREATE_DATASELFBACKUP_DBMGR_IOC = 10036,      // 创建 ncIEVFSDataSelfBackupDBMgr 对象失败
    NCT_CAN_NOT_SET_SITE_MASTEROSS_REPEATEDLLY = 10037,         // 不能重复设置站点的主存储
    NCT_FAILED_TO_SET_TAG_MAX_NUM = 10038,                      // 设置标签数量错误，必须为大于0，小于等于1000的整数
    NCT_FAILED_TO_CREATE_USER_DOWNLOAD_DBMGR_IOC = 10039,       // 创建 ncIETSUserDownloadDBMgr 对象失败
    NCT_NAME_CONTAINS_INVALID_CHAR = 10040,                     // 名称包含无效字符
    NCT_CID_OBJECT_NOT_EXIST = 10041,                           // 管理对象不存在
    NCT_GNS_OBJECT_NOT_EXIST = 10042,                           // gns對象不存在
    NCT_ERR_INVALID_OBJECT_TYPE = 10043,                        // 不正确的操作对象
    NCT_FAILED_TO_CREATE_EVFS_NAME_IOC = 10044,                 // 创建 ncIEVFSNameIOC 对象失败
    NCT_FAILED_TO_CREATE_DOCFAVORITES_IOC = 10045,              // 创建ncEVFSDocFavoritesIOC对象失败
    NCT_FAILED_TO_COPY_FILE_FROM_WATERMARK_DOC = 10046,         // 无法复制出水印目录
    NCT_INVALID_SUFFIXES = 10047,                               // 非法的后缀字符串
    NCT_CANNOT_FIND_SITE_STOR_INFO = 10048,                     // 无法找到该站点存储信息
    NCT_FAILED_TO_CREATE_ENTRY_DOC_MANAGER = 10049,             // 创建 ncIEntryDocManager 对象失败
}

/**
 * EVFS 管理服务接口
 */
service ncTEVFS {

    /////////////////////////////////////////////////////////////////////////////////////
    //
    // 以下接口提供上层应用访问使用
    // 若EOFS尚未加载，则自动加载
    // 若EOFS尚未初始化，则抛错
    //

    //
    // GNS 对象访问管理
    //

    /**
     * 创建 管理 对象
     *
     * @param userId: 用户id
     * @param name:    名字
     * @return 该名字对应的gns
     * @throw 转抛内部调用异常
     */
    string CreateMgrObject (1: string userId, 2: string name)
                            throws (1: EThriftException.ncTException exp),

    /**
    * 还原 管理 对象
    *
    * @param gns:    gns路径
    * @throw 转抛内部调用异常；
    *          若指定的不是 CID 管理对象，抛出异常提示。
    */
    void RestoreMgrObject (1: string gns)
                        throws (1: EThriftException.ncTException exp),

    /**
     * 删除 管理 对象
     *
     * @param gns:    gns路径
     * @param mark:  false,彻底删除 true,标记删除
     * @throw 转抛内部调用异常；
     *          若指定的不是 CID 管理对象，抛出异常提示。
     */
    void RemoveMgrObject (1: string gns, 2: bool mark)
                          throws (1: EThriftException.ncTException exp),

    /**
     * 迁移 管理 对象
     *
     * @param userId: 用户id
     * @param gnsObjects:    需迁移的对象集
     * @param targetPath:    迁移的目标路径
     * @throw 转抛内部调用异常；
     *          若对象集成员或者目标对象不是 CID 管理对象，抛出异常提示。
     */
    void MoveMgrObjects (1: string userId, 2: ncTEVFSGNSObjectSet cidObjects, 3: string targetPath)
                         throws (1: EThriftException.ncTException exp),

    /**
     * 检查对象是否存在
     *
     * @param gns:    gns路径
     * @throw 转抛内部调用异常；
     *          若指定的对象不存在，抛出异常提示。
     */
    bool ObjectExists (1: string gns)
                       throws (1: EThriftException.ncTException exp),

    /**
     * 获取根对象的子对象集
     *
     * @throw 转抛内部调用异常。
     */
    ncTEVFSGNSObjectSet GetSubObjectSet ()
                                         throws (1: EThriftException.ncTException exp),

    /**
     * 创建目录
     *
     * @param gns: 父对象gns路径
     * @param dirName: 目录名称
     * @throw 转抛内部调用异常；
     *        若gns不是 CID 管理对象或目录对象，抛出异常提示。
     *        若存在同名对象，抛出异常提示。
     */
    void CreateDir (1: string gns, 2: string dirName)
                    throws (1: EThriftException.ncTException exp),

    /**
     * 获取子目录集，无权限检查
     *
     * @param gns: 父目录gns路径
     * @return 子目录集
     * @throw 转抛内部调用异常；
     *        若gns不是 CID 管理对象或目录对象，抛出异常提示。
     */
    ncTEVFSGNSObjectSet ListDirWithoutPermCheck (1: string gns)
                    throws (1: EThriftException.ncTException exp),

    /**
     * 获取子文件集，无权限检查
     *
     * @param gns: 父目录gns路径
     * @return 子文件集
     * @throw 转抛内部调用异常；
     *        若gns不是 CID 管理对象或目录对象，抛出异常提示。
     */
    ncTEVFSGNSObjectSet ListFileWithoutPermCheck (1: string gns)
                    throws (1: EThriftException.ncTException exp),

    /**
     * 复制文件或目录，无权限检查
     *
     * @param userId: 用户id
     * @param srcGns: 源gns
     * @param newParentGns: 目的gns
     * @param ondup: 1:检查充满冲突，2：自动重命名，3：覆盖
     * @return 复制后文件或目录的gns
     * @throw 转抛内部调用异常
     */
    string CopyWithoutPermCheck (1: string userId, 2: string srcGns, 3: string newParentGns, 4: i32 ondup)
                    throws (1: EThriftException.ncTException exp),

    /**
     * 检查 管理对象 下面是否有数据
     *
     * @param gns: gns路径
     * @return 若管理对象下面无数据（除回收站以外），且回收站下面也无数据，返回true；否则返回false
     * @throw 转抛内部调用异常；
     *          若指定的不是 CID 管理对象，抛出异常提示。
     */
    bool CheckMgrObjectEmpty (1: string gns)
                              throws (1: EThriftException.ncTException exp),

    /**
     * 检查 管理对象 下面除回收站以外是否有数据
     *
     * @param gns: gns路径
     * @return 若管理对象下面无数据（除回收站以外），返回true；否则返回false
     * @throw 转抛内部调用异常；
     *          若指定的不是 CID 管理对象，抛出异常提示。
     */
    bool CheckMgrObjectEmptyWithoutRecycleBin (1: string gns)
                              throws (1: EThriftException.ncTException exp),


    /**
     * id组成的gns转换name组成的gns
     *
     * @param gns: gns路径
     * @return name组成的gns
     * @throw 转抛内部调用异常。
     */
    string ConvertPath (2: string gns)
                        throws (1: EThriftException.ncTException exp),

    /**
     * 批量把id组成的gns转换name组成的gns，若对应的key值gns不存在，value值为空
     * @param gnsList : 待转化的gns列表
     * @return map<gnsById(id形式), gnsByName(转化后的name形式)>,若待转化的gns对象不存在,则不出现于返回的map中
     */
    map<string, string> ConvertPathByBatch (1: list<string> gnsList)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * name组成的gns转换id组成的gns
     *
     * @param gns: name组成的gns
     * @return gns路径
     * @throw 转抛内部调用异常
     *        若某一级路径名不存在，抛出参数异常 10001
     *        若某一级路劲下存在同名重复文件，抛出对象不唯一异常 10023
     */
    string ConvertNamePath (1: string gns)
                            throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件多版本的最大个数
     * @param maxNum:    范围必须是[1, 64]
     *
     * @throw 转抛内部调用异常。
     * note: 当前版本不支持修改立即生效，需重启服务才生效
     */
    void SetVersionMaxNum (1: i32 maxNum)
                           throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件多版本的最大个数，默认为32个
     *
     * @throw 转抛内部调用异常。
     */
    i32 GetVersionMaxNum ()
                          throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件多版本的生成周期，单位为分钟
     * @param buildCycle:    范围必须是[1, 60]
     *
     * @throw 转抛内部调用异常。
     * note: 当前版本不支持修改立即生效，需重启服务才生效
     */
    void SetVersionBuildCycle (1: i32 buildCycle)
                               throws (1: EThriftException.ncTException exp),

    // 获取文件多版本的生成周期，默认为5分钟
    i32 GetVersionBuildCycle ()
                              throws (1: EThriftException.ncTException exp),

    // 设置标签的最大个数
    void SetTagMaxNum (1: i32 maxNum)
                       throws (1: EThriftException.ncTException exp),

    // 获取标签的最大数量，默认为30个
    i32 GetTagMaxNum ()
                      throws (1: EThriftException.ncTException exp),

    // 设置是否在外链中使用提取码
    void SetLinkAccessCodeStatus (1: bool enable)
                                  throws (1: EThriftException.ncTException exp),

    // 获取是否在外链中使用提取码
    bool GetLinkAccessCodeStatus ()
                                  throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 文件点评功能设置
    //

    /**
     * 获取文件评论功能状态
     *
     * @return: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    bool GetDocCommentStatus ()
                              throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件评论功能状态
     *
     * @param enable: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    void SetDocCommentStatus (1: bool enable)
                              throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件评分功能状态
     *
     * @return: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    bool GetDocScoreStatus ()
                            throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件评分功能状态
     *
     * @param enable: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    void SetDocScoreStatus (1: bool enable)
                            throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件评论、评分是否开启的状态，其中一个开启，即为功能开启
     *
     * @param enable: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    bool GetDocCommentConfigStatus ()
                                    throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 限制大文件上传，限制文件类型上传
    //

    // 设置大文件传输限制
    void SetLargeFileLimit (1: ncTEVFSLargeFileLimitConf conf)
                            throws (1: EThriftException.ncTException exp),

    // 获取大文件传输限制配置信息
    ncTEVFSLargeFileLimitConf GetLargeFileLimit ()
                                                 throws(1: EThriftException.ncTException exp)

    // 设置限制上传的文件类型配置
    void SetFileSuffixLimit (1: list<ncTLimitSuffixDoc> suffixDocs) throws (1: EThriftException.ncTException exp),

    // 获取限制上传的文件类型配置
    list<ncTLimitSuffixDoc> GetFileSuffixLimit () throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 获取gns的基本信息
    //
    /**
     * 获取ETS资源对象信息
     **/
     ncTETSResourceInfo GetETSResourceInfo (1: string gns)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 批量获取资源对象信息
     * @param gnsList : 传入待查询的对象gns路径
     * @return 返回查询到的资源对象信息映射表<gns, 资源信息>,若gns对象为管理对象，其下未上传文件/目录时，返回otag为空
     */
    map<string, ncTResourceInfo> GetAllResourceInfo (1: list<string> gnsList)
                                                     throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    // 内存缓存部分
    //

    /**
     * 重置浏览缓存
     *
     * @throw 转抛内部调用异常
     */
    void ResetListCache ()
                         throws (1: EThriftException.ncTException exp),

    /**
     * 启用浏览缓存
     *
     * @throw 转抛内部调用异常
     */
    void EnableListCache ()
                          throws (1: EThriftException.ncTException exp),

    /**
     * 禁用浏览缓存
     *
     * @throw 转抛内部调用异常
     */
    void DisableListCache ()
                           throws (1: EThriftException.ncTException exp),

    /**
     * 启用浏览缓存统计
     *
     * @throw 转抛内部调用异常
     */
    void EnableListCacheStats ()
                               throws (1: EThriftException.ncTException exp),

    /**
     * 禁用浏览缓存统计
     *
     * @throw 转抛内部调用异常
     */
    void DisableListCacheStats ()
                                throws (1: EThriftException.ncTException exp),

    /**
     * 获取浏览缓存统计
     *
     * @throw 转抛内部调用异常
     */
    ncTEVFSListCacheInfo FetchListCacheInfo ()
                                             throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////////////////////////////////////
    //
    // 文件统计部分
    //

    /**
     * 获取当前时刻系统中文件的总量和各种分类项目的数量
     *
     * @return ncTEVFSFilesCount: 表示统计文件的数量(由不同类目组成)
     * @throw 转抛内部调用异常
     */
    ncTEVFSFilesCount GetCurrentFilesTotal ()
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 获取截止到指定日期单位，系统中文件的总量
     * @param date : 截止日期
     * @param dateUnit : 指定查询的单位 (日、月、年)
     * @return i32 : 表示时刻编号(从1开始)，编号1表示[0-1]这个时间段，间距为1小时/天/月，以此类推。另，如果时间是未来的时间，则不返回相关信息
     * @return ncTEVFSFilesCount: 表示统计文件的数量(由不同类目组成)
     */
    map<i32, ncTEVFSFilesCount> GetFilesTotal (1: ncTEVFSDate date, 2: ncTEVFSDateUnit dateUnit)
                                               throws (1: EThriftException.ncTException exp),

    /**
     * 获取指定日期范围内，系统文件的变化情况
     * @param date : 指定日期范围
     * @param dateUnit : 指定日期的单位
     * @return i32 : 1. dateUnit为日: 表示时刻编号(从1开始)，编号1表示[0-1]这个时间段，间距为1小时，以此类推
     *               2. dateUnit为月: 表示日编号(从1开始)，编号1表示第一天，间距为1天，以此类推。
     *               3. dataUnit为年: 表示月编号(从1开始)，编号1表示第一个月，间距为1月，以此类推。
     *               另，如果时间是未来的时间，则不返回相关信息
     * @return ncTEVFSFilesChanged: 表示统计文件变化的数量(包含不同类目)
     */
     map<i32, ncTEVFSFilesChanged> GetFilesChangeInfo (1: ncTEVFSDate date, 2: ncTEVFSDateUnit dateUnit)
                                                       throws (1: EThriftException.ncTException exp),


    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 空间配额部分
    //
    /**
     * 获取配额空间的信息
     * @param strCid : 资源容器cid
     * @return ncTEVFSQuotaInfo : 该用户的配额空间的信息(配额空间的大小、已使用的大小、临时超额的大小)
     * @throw 转抛内部调用异常
     */
    ncTEVFSQuotaInfo FetchSpaceQuotaInfo (1: string cidGns)
                                          throws (1: EThriftException.ncTException exp),


    /**
     * 设置配额空间的大小
     * @param strCid : 资源容器cid
     * @param quota: 指定配额空间的大小(单位:Byte)
     * @throw 转抛内部调用异常
     */
    void SetQuotaInfo (1: string cidGns, 2: i64 quota)
                       throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    // 操作统计部分
    //
    /**
     * 查询某个操作的执行次数
     * @param begDate : 起始查询时间
     * @param endDate : 终止查询时间
     * @param opType : 操作类型
     * @throw 转抛内部调用异常
     */
    i64 FetchOperatedInfo (1: ncTEVFSDate begDate, 2: ncTEVFSDate endDate, 3: ncTEVFSOperatedType opType)
                           throws (1: EThriftException.ncTException exp),

    /**
     * 查询所有操作的执行次数
     * @param begDate : 起始查询时间
     * @param endDate : 终止查询时间
     * @return : first 表示操作类型，second表示操作总量
     * @throw 转抛内部调用异常
     */
    map<ncTEVFSOperatedType, i64> FetchAllOperatedInfo (1: ncTEVFSDate begDate, 2: ncTEVFSDate endDate)
                                                        throws (1: EThriftException.ncTException exp),


    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 秒传开关部分
    //
    /**
     * 判断是否支持秒传功能
     * @return : 是否支持秒传功能
     * @throw 转抛内部调用异常
     */
    bool GetRapidUploadSupport ()
                                throws (1: EThriftException.ncTException exp),

    /**
     * 设置是否支持秒传功能
     * @support : 是否支持秒传功能
     * @throw 转抛内部调用异常
     */
    void SetRapidUploadSupport (1: bool support)
                                throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 多站点秒传开关部分
    //
    /**
     * 判断多站点开关是否开启
     * @return : 是否开启多站点秒传
     * @throw 转抛内部调用异常
     */
    bool GetMultiSiteRapidUploadSwitch ()
                                throws (1: EThriftException.ncTException exp),

    /**
     * 设置多站点秒传开关
     * @enable : 是否开启多站点秒传
     * @throw 转抛内部调用异常
     */
    void SetMultiSiteRapidUploadSwitch (1: bool enable)
                                throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 秒传统计部分
    //
    /**
     * 查询秒传统计信息
     * @return : 秒传的统计信息
     * @throw 转抛内部调用异常
     */
    ncTEVFSRapidStatisInfo FetchRapidStatisInfo ()
                                                 throws (1: EThriftException.ncTException exp),


    /**
     * 查询秒传文件个数
     * @param fileName :    文件名,查询的正则表达式为: *fileName*
     * @param fileSizeMin : 起始大小(字节,闭区间) 范围[0, 9223372036854775807]
     * @param fileSizeMax : 终止大小(字节,闭区间) 范围[0, 9223372036854775807]
     * @param beginDate : 起始日期时间戳(精确到毫秒，闭区间)
     * @param endDate : 终止日期时间戳(精确到毫秒，闭区间)
     * @return : 秒传文件个数
     * @throw 转抛内部调用异常
     */
    i64 FetchTotalRapidFile (1: string fileName,
                             2: i64 fileSizeMin,
                             3: i64 fileSizeMax,
                             4: i64 beginDate,
                             5: i64 endDate)
                             throws (1: EThriftException.ncTException exp),


    /**
     * 查询秒传统计信息
     * @param fileName :    文件名,查询的正则表达式为: *fileName*
     * @param fileSizeMin : 起始大小(字节,闭区间) 范围[0, 9223372036854775807]
     * @param fileSizeMax : 终止大小(字节,闭区间) 范围[0, 9223372036854775807]
     * @param beginDate : 起始日期时间戳(精确到毫秒，闭区间)
     * @param endDate : 终止日期时间戳(精确到毫秒，闭区间)
     * @param offset : 偏移值(从0开始)
     * @param rows : 获取的行数(小于500,减少服务端内存的使用)
     * @return : 秒传文件信息列表
     * @throw 转抛内部调用异常
     */
    list<ncTEVFSRapidFileInfo> FetchRapidFilesInfo (1: string fileName,
                                                    2: i64 fileSizeMin,
                                                    3: i64 fileSizeMax,
                                                    4: i64 beginDate,
                                                    5: i64 endDate,
                                                    6: i64 offset,
                                                    7: i32 rows)
                                                    throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件密级
     *
     * @param gns:    gns路径
     * @throw 转抛内部调用异常；
     *          若指定的对象不存在，或者不是文件，抛出异常提示。
     */
    i32 GetCSFLevel (1: string gns)
                     throws (1: EThriftException.ncTException exp),

    /**
     * 根据gns获取文件密级或文件夹下子对象最高密级
     *
     * @param gns:       gns路径
     * @return   :       文件密级或文件夹下子对象最高密级
     * @throw 转抛内部调用异常；
     *          若指定的对象不存在，或者gns为管理对象，抛出异常提示。
    */
    i32 GetDirCSFLevel (1: string gns)
                            throws (1: EThriftException.ncTException exp),

    /**
     * 设置密级
     *
     * @param gns            : 目录或文件对象的 gns 路径
     * @param csfLevel       : 设置的密级值
     * @param userCsfLevel   : 用户的密级值
     * @param userId         : 定密审核员ID，当对象为文件时，用于记录定密的责任人和部门信息
     * @throw 转抛内部调用异常；
     *        若指定的对象不存在，或者不是目录或文件，抛出异常提示。
     */
    void SetCsfLevel (1: string gns, 2: i32 csfLevel, 3: i32 userCsfLevel, 4: string userId)
                      throws (1: EThriftException.ncTException exp),

    /**
     * 获取所有开启了外链的用户id
     *
     * @return :    开启了外链的用户id列表
     * @throw 转抛内部调用异常。
     */
    list<string> GetLinkOwnerIds ()
                                  throws (1: EThriftException.ncTException exp),

    /**
     * 删除一个用户的所有外链
     *
     * @param userId:    用户id
     * @throw 转抛内部调用异常。
     */
    void DeleteLinkByUserId (1: string userId)
                             throws (1: EThriftException.ncTException exp),

    /**
     * 删除一个用户的所有收藏
     *
     * @param userId:    用户id
     * @throw 转抛内部调用异常。
     */
    void DeleteFavoritesByUserId (1: string userId)
                             throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 对象存储服务部分
    //

    /**
     * 获取第三方对象存储服务信息
     *
     * @return :    使用的第三方对象存储信息
     * @throw 转抛内部调用异常。
     */
    ncTEVFSOSSInfo GetThirdPartyOSSInfo ()
                               throws (1: EThriftException.ncTException exp),

    /**
     * 设置第三方对象存储服务信息
     *
     * @param ossInfo:    对象存储服务信息
     * @throw 转抛内部调用异常。
     */
    void SetThirdPartyOSSInfo (1: ncTEVFSOSSInfo ossInfo)
                               throws (1: EThriftException.ncTException exp),

    /**
     * 设置 EOSS 账户信息
     *
     * @param ossInfo:    对象存储服务信息
     * @throw 转抛内部调用异常。
     */
    void SetEOSSAccessInfo (1: ncTEVFSOSSInfo ossInfo)
                            throws (1: EThriftException.ncTException exp),

    /**
     * 设置本节点第三方对象存储服务信息
     *
     * @param ossInfo:    对象存储服务信息
     * @throw 转抛内部调用异常。
     */
    void UpdateLocalThirdPartyOSSInfo ()
                                       throws (1: EThriftException.ncTException exp),

    /**
     * 验证第三方对象存储服务是否可以通信
     *
     * @param ossInfo:    对象存储服务信息
     * @throw 转抛内部调用异常。
     */
    bool ConnectThirdPartyOSS (1: ncTEVFSOSSInfo ossInfo)
                               throws (1: EThriftException.ncTException exp),


    // 获取所有对象存储服务信息
    map<string, ncTEVFSOSSInfo> GetOSSInfo ()
                                            throws (1: EThriftException.ncTException exp),

    // 设置对象存储服务信息
    void SetOSSInfo (1: ncTEVFSOSSInfo ossInfo)
                     throws (1: EThriftException.ncTException exp),

    // 配置站点的主存储 id
    void SetSiteMasterOSS (1: string siteId, 2: string masterOSSId)
                           throws (1: EThriftException.ncTException exp),

    // 配置站点的备份存储 id
    void SetSiteSyncToOSS (1: string siteId, 2: string syncToOSSId)
                           throws (1: EThriftException.ncTException exp),

    // 配置站点的主备存储的角色互换 1：使用主存储作为AS存储 2: 使用备份存储作为AS存储
    void SetSiteStorageRoleStatus (1: string siteId, 2: i32 status)
                                        throws (1: EThriftException.ncTException exp),

    // 配置站点存储同步模式 0: 不同步 1: 单向同步（由使用中存储向备用存储同步） 2: 双向同步 （两个存储互相同步数据）
    void SetSiteSyncMode (1: string siteId, 2: i32 mode)
                           throws (1: EThriftException.ncTException exp),

    // 配置站点存储 （SetSiteMasterOSS、SetSiteSyncToOSS、SetSiteStorageRoleStatus、SetSiteSyncMode合一）
    void SetSiteOSS (1: string siteId, 2: string masterOSSId, 3: string syncToOSSId, 4: i32 status, 5: i32 mode)
                                            throws (1: EThriftException.ncTException exp),

    // 获取站点使用的对象存储服务信息
    map<string, ncTEVFSSiteOSS> GetSiteOSSInfo ()
                                                    throws (1: EThriftException.ncTException exp),

    // 更新本节点站点使用的对象存储服务信息
    void UpdateLocalSiteOSSMap ()
                                throws (1: EThriftException.ncTException exp),


    // 更新站点使用的反向代理信息
    void UpdateSiteProxyMap ()
                             throws (1: EThriftException.ncTException exp),

    // 更新本节点站点使用的反向代理信息
    void UpdateLocalSiteProxyMap ()
                                  throws (1: EThriftException.ncTException exp),

    /**
     * 设置 OSS 所用的主机名 (当存储使用EOSS时生效)
     *
     * @param hostName:    主机名
     * @throw 转抛内部调用异常。
     */
    void SetOSSHostName (1: string hostName)
                         throws (1: EThriftException.ncTException exp),

    /**
     * 设置 OSS 所用的端口 (当存储使用EOSS时生效)
     *
     * @param httpsPort:    https 端口
     * @param httpPort :    http  端口
     * @throw 转抛内部调用异常
     *        若参数为负值
     */
    void SetOSSPorts (1: i32 httpsPort, 2: i32 httpPort)
                      throws (1: EThriftException.ncTException exp),

    /**
     * 更新 OSS 所用的站点信息 (当存储使用EOSS时生效)
     *
     * @param siteInfo :    站点信息，map的key为站点的uuid
     * @throw 转抛内部调用异常
     *        若参数为负值
     */
    void UpdateSiteInfo (1: map<string, ncTEVFSSiteEossInfo> siteInfo)
                         throws (1: EThriftException.ncTException exp),

    /**
     * 获取开放存储的分块大小
     *
     * 返回值小于等于4194304时，按照4M大小分块
     * 返回值大于4194304时，按照返回值大小分块
     *
     * @return : 返回分块的最小值，单位byte
     * @throw 转抛内部调用异常
     */
    i64 GetOSSSizeInfo ()
                        throws (1: EThriftException.ncTException exp),

    /**
     * 开放存储单次上传文件 (上传不大于64M的文件)
     *
     * @param cid : 存储的管理id
     * @param objectId : 存储的对象id
     * @param siteId: 站点id，默认为空
     * @return : 分块上传请求的method, url, headers
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetUploadInfo (1: string cid, 2: string objectId, 3: string siteId)
                                     throws (1: EThriftException.ncTException exp),

    /**
     * 初始化开放存储分块上传
     *
     * @param cid : 存储的管理id
     * @param objectId : 存储的对象id
     * @param siteId: 站点id，默认为空
     * @return : 分块上传的id
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    string InitMultiUpload (1: string cid, 2: string objectId, 3: string siteId, 4: bool isExternalReq)
                            throws (1: EThriftException.ncTException exp),

    /**
     * 获取开放存储上传分块的请求
     *
     * @param cid : 存储的管理id
     * @param objectId : 存储的对象id
     * @param siteId: 站点id，默认为空
     * @param uploadId : 上传id
     * @param partNum : 分块号
     * @return : 分块上传请求的method, url, headers
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetMultiUploadInfo (1: string cid, 2: string objectId, 3: string siteId, 4: string uploadId, 5: i32 partNum, 6: bool isExternalReq)
                                          throws (1: EThriftException.ncTException exp),

    /**
     * 完成开放存储分块上传
     *
     * @param cid : 存储的管理id
     * @param objectId : 存储的对象id
     * @param siteId: 站点id，默认为空
     * @param uploadId : 上传id
     * @param partInfos : 已经上传的分块信息
     * @return : 完成分块上传请求的method, url, headers, body
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetCompleteMultiUploadInfo (1: string cid, 2: string objectId, 3: string siteId, 4: string uploadId, 5: map<i32, ncTEVFSOSSPartInfo> partInfos, 6: bool isExternalReq)
                                                  throws (1: EThriftException.ncTException exp),

   /**
     * 获取开放存储的下载请求
     *
     * @param cid: 存储的管理id
     * @param objectId: 存储的对象id
     * @param siteId: 站点id，默认为空
     * @param reqHost: 从存储服务下载的请求地址
     * @param useHttps: 是否使用https下载
     * @param validSeconds: 下载请求的有效时长
     * @param fileName: 浏览器下载的默认保存文件名，参数为空时不设置该项
     * @param fileSize: 单次上传创建的文件，需给出文件大小；分块上传创建的文件，该项选填，不给实际大小时传参数 -1
     * @param isExternalReq: 如果为true，返回外部下载请求；如果为false，返回内部下载请求 (对于EOSS，ip为127.0.0.1)
     * @return : 下载请求的method, url, headers
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetDownloadInfo (1: string cid,
                                       2: string objectId,
                                       3: string siteId,
                                       4: string reqHost,
                                       5: bool useHttps,
                                       6: i64 validSeconds,
                                       7: string fileName,
                                       8: i64 fileSize,
                                       9: bool isExternalReq)
                                       throws (1: EThriftException.ncTException exp),

   /**
     * 获取开放存储的删除请求
     *
     * @param cid: 存储的管理id
     * @param objectId: 存储的对象id
     * @param siteId: 站点id，默认为空
     * @return : 删除请求的method, url, headers
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetDeleteInfo (1: string cid, 2: string objectId, 3: string siteId)
                                     throws (1: EThriftException.ncTException exp),

   /**
     * 获取开放存储的查询请求
     *
     * @param cid: 存储的管理id
     * @param objectId: 存储的对象id
     * @param siteId: 站点id，默认为空
     * @return : 查询请求的method, url, headers
     * @throw 转抛内部调用异常
     *        若cid或objectId 不为GUID
     */
    ncTEVFSOSSRequest GetHeadInfo (1: string cid, 2: string objectId, 3: string siteId)
                                   throws (1: EThriftException.ncTException exp),

    /**
     * 下载时设置对象存储鉴权后url有效时间
     *
     * @param validSeconds: 返回鉴权后url的有效时间
     * @throw 转抛内部调用异常
     */
     void SetAuthenticationDownloadValidSeconds(1: i64 validSeconds)
                          throws (1: EThriftException.ncTException exp),

    /**
     * 下载时获取对象存储鉴权后url有效时间
     *
     * @return ： 返回url的有效时间
     * @throw 转抛内部调用异常
     */
     i64 GetAuthenticationDownloadValidSeconds()
                          throws (1: EThriftException.ncTException exp),


    /**
     * 上传时设置获取对象存储鉴权后url有效时间
     *
     * @param validSeconds: 返回鉴权后url的有效时间
     * @throw 转抛内部调用异常
     */
     void SetAuthenticationUploadValidSeconds(1: i64 validSeconds)
                          throws (1: EThriftException.ncTException exp),

    /**
     * 上传时获取对象存储鉴权后url有效时间
     *
     * @return：返回url的有效时间
     * @throw 转抛内部调用异常
     */
     i64 GetAuthenticationUploadValidSeconds()
                          throws (1: EThriftException.ncTException exp),


    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 文件自定义属性管理
    //

    /**
      * 获取所有自定义属性
      *
      * @throw 转抛内部调用异常
      */
    list<ncTEVFSCustomAttribute> ListAttributes()
                                                throws (1: EThriftException.ncTException exp),

    /**
      * 添加一条自定义属性
      *
      * @param pro: 需要添加的属性
      * @throw 转抛内部调用异常
      *        属性重名
      */
    void AddAttribute(1: ncTEVFSCustomAttribute pro)
                      throws (1: EThriftException.ncTException exp),

    /**
      * 修改一条自定义属性
      *
      * @param pro: 需要修改的属性
      * @throw 转抛内部调用异常
      */
    void SetAttribute(1: ncTEVFSCustomAttribute pro)
                      throws (1: EThriftException.ncTException exp),

    /**
      * 删除一条自定义属性
      *
      * @param id: 需要删除的属性ID
      * @throw 转抛内部调用异常
      */
    void DelAttribute(1: i64 id)
                      throws (1: EThriftException.ncTException exp),

    /**
      * 设置自定义属性状态
      *
      * @param status: 0：隐藏 1:显示
      * @throw 转抛内部调用异常
      */
    void SetAttributeStatus (1: i64 id, 2: i32 status)
                             throws (1: EThriftException.ncTException exp),

    /**
      * 获取属性值
      *
      * @param id: 属性ID
      * @return: 以JSON格式返回
      *          例： [{"name": "asd", "child": [{"name": "asd1"}] }]
      * @throw 转抛内部调用异常
      */
    string GetAttributeValue(1: i64 id)
                            throws (1: EThriftException.ncTException exp),

    /**
      * 设置文档预览转换开关
      *
      * @param enable: true--开启， false--关闭
      * @throw 转抛内部调用异常
      */
    void SetPreConvertEnable(1: bool enable)
                            throws (1: EThriftException.ncTException exp),


    //////////////////////////////////////////////////////////
    //
    // 对象元数据中的应用管理
    //

    /**
      * 增加应用信息，默认状态为启用
      *
      * @param appId: 应用ID，可以为空，为空时服务内部生成应用id；格式为 uuid，如 7270a9fb-ce86-400f-8c0c-7d48b5790b1b
      * @param appName: 应用名
      */
    void ObjMeta_AddAppInfo (1: string appId,
                             2: string appName)
                             throws (1: EThriftException.ncTException exp),

    /**
     * 获取所有应用信息
     * @return: 应用信息的 map，key 为应用 id
     */
    map<string, ncTEVFSObjMetaAppInfo> ObjMeta_GetAppInfos ()
                                                            throws (1: EThriftException.ncTException exp),

    /**
      * 根据应用id，设置应用名
      *
      * @param appId: 应用ID
      * @param appName: 应用名
      */
    void ObjMeta_SetAppName (1: string appId,
                             2: string appName)
                             throws (1: EThriftException.ncTException exp),

    /**
      * 根据应用id，设置应用状态
      *
      * @param appId: 应用ID
      * @param status: 应用状态
      */
    void ObjMeta_SetAppStatus (1: string appId,
                               2: i32 status)
                               throws (1: EThriftException.ncTException exp),

    /**
      * 删除应用信息
      *
      * @param appId: 应用ID
      */
    void ObjMeta_DeleteAppInfo (1: string appId)
                                throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 数据自备份管理
    //

    // 获取数据自备份配置
    ncTEVFSDataSelfBackupConfig GetDataSelfBackupConfig ()
                                                         throws (1: EThriftException.ncTException exp),

    // 配置数据自备份功能
    void SetDataSelfBackupConfig (1: ncTEVFSDataSelfBackupConfig config)
                                  throws (1: EThriftException.ncTException exp),

    // 获取数据自备份的进度
    map<string, string> GetDataSelfBackupProgress ()
                                                   throws (1: EThriftException.ncTException exp),

    // 立即开始一次数据同步
    void SelfBackupManualStart (1: string siteId)
                                throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 限制用户的文档下载量
    //

    // 配置是否开启限制
    void SetUserDownloadLimitStatus (1: bool enable)
                                  throws (1: EThriftException.ncTException exp),

    // 获取是否开启限制的状态
    bool GetUserDonwloadLimitStatus ()
                                  throws (1: EThriftException.ncTException exp),

    // 添加用户文档下载量限制信息，如果用户记录存在则更新文档限制量
    void AddUserDownloadLimitInfos (1: list<ncTUserDownloadLimitInfo> limitInfos)
                                   throws (1: EThriftException.ncTException exp),

    // 获取用户文档下载量限制信息
    list<ncTUserDownloadLimitInfo> GetUserDownloadLimitInfos ()
                                                              throws (1: EThriftException.ncTException exp),

    // 删除用户文档下载量限制信息
    void DeleteUserDownloadLimitInfos (1: list<string> userIds)
                                       throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 隔离区管理
    //

    // 列举隔离区
    list<ncTEVFSQuarantineFileInfo> GetQuarantineFileList (1: ncTFiltrationParam filter, 2: i64 start, 3: i64 limit)
                                                                   throws (1: EThriftException.ncTException exp),

    // 根据文件docid获取文件在隔离区中的版本
    list<ncTEVFSQuarantineFileInfo> GetFileVersionList (1: string docid, 2: string key)
                                                                    throws (1: EThriftException.ncTException exp),

    // 列举隔离区
    i64 GetQuarantineFileCount (1: ncTFiltrationParam filter)
                                          throws (1: EThriftException.ncTException exp),

    // 下载文件
    ncTOSDowndloadRetParam OSDownload (1: string gns, 2: string versionId, 3: string authType, 4: string reqHost, 5: bool usehttps, 6: string saveName)
                                                                   throws (1: EThriftException.ncTException exp),


    /**
     * 还原隔离区文件
     *
     * @param ondup:
     * 1:检查是否重命名，重名则抛异常
     * 2:如果重名冲突，自动重名
     * @retuen : 还原后的全路径
     * @throw 转抛内部调用异常
     */
    string RestoreQuarantineFile (1: string gns, 2: i32 ondup)
                                          throws (1: EThriftException.ncTException exp),


    // 删除隔离区文件
    string DeleteQuarantineFile (1: string gns)
                                throws (1: EThriftException.ncTException exp),

    /**
     * 隔离
     *
     * @param docId: 要隔离的文件gns，未隔离的文件会将整个文件隔离，已隔离的文件会将该版本标记隔离
     * @param reason: 隔离原因
     * @param type: 隔离类型
     * @return: 日志所需资源（cid一级为ID，路径到文件一级）
     * @throw 转抛内部调用异常
     */
    ncTQuarantineRetMsg Quarantine (1: string docId, 2: string reason 3: ncTEVFSQuarantineType type)
                          throws (1: EThriftException.ncTException exp),

    // 获取隔离区配置
    ncTQuarantineConfig QRT_GetConfig()
                                throws (1: EThriftException.ncTException exp),

    // 设置申诉保护时间,以天为单位
    void QRT_SetAppealProtectTime (1: i32 days)
                                throws (1: EThriftException.ncTException exp),


    // 设置自动时间,以天为单位 (-1 关闭功能)
    void QRT_SetAutoDeleteTime (1: i32 days)
                                throws (1: EThriftException.ncTException exp),

    /**
     * 审核申诉
     *
     * @param ondup:
     * 1:检查是否重命名，重名则抛异常
     * 2:如果重名冲突，自动重名
     * @param appealSuggest: 申诉的处理意见
     * @return : 重命名之后的名字
     * @throw 转抛内部调用异常
     */
    string QRT_AppealApproval (1: string docid, 2: bool approvalResult, 3: i32 ondup, 4: string appealSuggest)
                                    throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 外链留底文件搜索
    //

    /**
     * 获取外链访问信息总数
     *
     * @param name: 文件名，模糊匹配
     * @return : 外链访问信息总数
     * @throw 转抛内部调用异常
     */
    ncTEVFSOutLinkAccessInfoCount GetOutLinkAccessInfoCount (1: string name)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 分页获取外链访问信息
     * 返回的结果按访问时间降序
     *
     * @param param: 分页获取外链访问信息参数
     * @return : 外链访问信息列表
     * @throw 转抛内部调用异常
     */
    list<ncTEVFSOutLinkAccessInfo> GetPageOutLinkAccessInfo (1: ncTEVFSGetPageOutLinkAccessInfoParam param)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 获取外链文件信息
     *
     * @param id: 记录id
     * @return : 外链文件信息
     * @throw 转抛内部调用异常
     */
    ncTEVFSOutLinkFileInfo GetOutLinkFileInfo (1: i64 id)
                                            throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 全局文件搜索
    //

    /**
     * 获取文件信息总数
     *
     * @param name: 文件名，模糊匹配
     * @return : 文件总数
     * @throw 转抛内部调用异常
     */
    ncTEVFSFileInfoCount GetFileInfoCount (1: string name)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 分页获取文件信息
     * 返回的结果按文件创建时间降序
     *
     * @param docId: 分页获取文件信息参数
     * @return : 文件信息列表
     * @throw 转抛内部调用异常
     */
    list<ncTEVFSFileInfo> GetPageFileInfo (1: ncTEVFSGetPageFileInfoParam param)
                                            throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件历史版本
     * 返回的结果按版本修改时间降序
     *
     * @param docId: 文件gns路径
     * @return : 文件历史版本列表
     * @throw 转抛内部调用异常
     */
    list<ncTEVFSFileMetadata> GetFileRevisions (1: string docId)
                                                throws (1: EThriftException.ncTException exp),

    //////////////////////////////////////////////////////////
    //
    // 站点与内网出口IP管理
    //

    /**
     * 根据内网出口IP获取站点
     *
     * @param ip: 内网出口IP，形式如下：192.168.137.42
     * @return : 站点Id
     * @throw 转抛内部调用异常
     */
     string GetSiteIdByIntranetIP (1: string intranetIP)
                                   throws (1: EThriftException.ncTException exp),

    /**
     * 设置站点的内网出口IP
     *
     * @param siteId: 站点Id
     * @param ip: 内网出口IP，形式如下：192.168.137.42
     * @throw 转抛内部调用异常
     */
     void SetIntranetIPOfSite (1: string siteId, 2: string intranetIP)
                               throws (1: EThriftException.ncTException exp),

    /**
     * 删除站点的内网出口IP
     *
     * @param siteId: 站点Id
     * @param ip: 内网出口IP，形式如下：192.168.137.42
     * @throw 转抛内部调用异常
     */
     void DeleteIntranetIPOfSite (1: string siteId, 2: string intranetIP)
                                  throws (1: EThriftException.ncTException exp),

    ////////////////////////////////////////////////////////////////////////////////////
    //
    // 文件到期提醒设置
    //

    /**
     * 获取文件到期提醒功能状态
     *
     * @return: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    bool GetDocDueRemindStatus ()
                                throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件到期提醒功能状态
     *
     * @param enable: true--开启， false--关闭
     * @throw 转抛内部调用异常。
     */
    void SetDocDueRemindStatus (1: bool enable)
                                throws (1: EThriftException.ncTException exp),

    /**
     * 获取文件到期提醒消息发送时间
     *
     * @return: 小时，24小时制
     * @throw 转抛内部调用异常。
     */
    i32 GetDocDueRemindMsgSendTime ()
                                    throws (1: EThriftException.ncTException exp),

    /**
     * 设置文件到期提醒消息发送时间
     *
     * @param hour: 仅允许小时，0-23
     * @throw 转抛内部调用异常。
     */
    void SetDocDueRemindMsgSendTime (1: i32 hour)
                                     throws (1: EThriftException.ncTException exp),
}
