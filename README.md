# LOOKKKEDU 18 社区版（中文版 README）

基于 Odoo 18 的教育场景插件集，统一品牌 LOOKKKEDU，覆盖招生、学籍、课表/考勤、考试、费用、图书馆、家长、活动、作业、设施/教室等，并提供网站主题与完整中文翻译。

## 模块与功能速览
- `openeducat_core`：核心数据/菜单（学生、教职工、课程、班级、学年学期、门户），学生证/在读证明报表。
- `openeducat_activity`：课外活动/社团。
- `openeducat_admission`：招生流程与分析报表。
- `openeducat_assignment`：作业布置/提交，自动化规则。
- `openeducat_attendance`：考勤登记/报表，联动课表。
- `openeducat_classroom`：教室与设施分配。
- `openeducat_exam`：考试/准考证/成绩单/成绩模板/考场编排。
- `openeducat_facility`：设施/设备管理。
- `openeducat_fees`：收费项目、学费条目、费用分析。
- `openeducat_library`：图书/媒体借阅、预约、条码、借阅卡。
- `openeducat_parent`：家长与亲属关系。
- `openeducat_timetable`：课表与时间段生成。
- `openeducat_activity`：活动与社团。
- `openeducat_erp`：整合安装包（一次安装主要功能）。
- `theme_web_openeducat`：网站/前端主题。

## 核心特性
- 招生/学籍/课程/考试/费用/考勤/图书馆/家校沟通一体化。
- 报表与证件：学生证、在读证明、借阅卡等（中文模板，兼容中文文件名）。
- 门户与角色：后台管理员、教职工、家长、学生门户权限，支持多组继承与域规则。
- 模块化扩展：按需安装，Odoo 18 权限/审计/国际化完备。

## 在线资源
- 官网/演示：<https://lookkkedu.com>
- 文档：<https://doc.lookkkedu.com/>

## 快速运行（Docker 示例）
1. 启动 Postgres（示例端口 5433 对外映射 5432）：
   ```bash
   docker run -d --name lookkkedu-db -p 5433:5432 \
     -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres \
     postgres:15
   ```
2. 启动 Odoo 18，挂载本仓库为额外插件：
   ```bash
   docker run -d --name lookkkedu-odoo --network host -p 8069:8069 \
     -v /path/to/LOOKKKEDU:/mnt/extra-addons \
     -e HOST=localhost -e PORT=5433 -e USER=odoo -e PASSWORD=odoo -e ADMIN_PASSWORD=admin \
     odoo:18 --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
   ```
3. 浏览器访问 `http://localhost:8069`，创建数据库后优先安装 `openeducat_core`，再按需安装其他模块或直接安装 `openeducat_erp`。

> 若已存在容器：`docker start lookkkedu-db lookkkedu-odoo`

## 升级/刷新翻译
示例（数据库名 `lookkkedu`，按需裁剪模块列表）：
```bash
docker exec lookkkedu-odoo odoo -c /etc/odoo/odoo.conf \
  --db_host=lookkkedu-db --db_port=5432 --db_user=odoo --db_password=odoo \
  -d lookkkedu \
  -u openeducat_core,openeducat_activity,openeducat_admission,openeducat_assignment,openeducat_attendance,openeducat_classroom,openeducat_exam,openeducat_facility,openeducat_fees,openeducat_library,openeducat_parent,openeducat_timetable,openeducat_erp \
  --stop-after-init
```
仅刷新核心/图书馆：`-u openeducat_core,openeducat_library`

## 常用报表/证件
- 学生证：`openeducat_core.report_student_idcard`
- 在读证明：`openeducat_core.report_student_bonafide`
- 借阅卡：`openeducat_library.report_student_library_card`

## 角色与权限
- 后台管理员：`openeducat_core.group_op_back_office_admin`
- 教职工：`openeducat_core.group_op_faculty`
- 家长管理员：`openeducat_parent.group_op_parent_manager`
- 门户家长/学生：`base.group_portal` + 家长模块规则
> 入口：设置 > 用户和公司 > 用户；开发者模式下可在 设置 > 技术 > 安全 > 组 查看继承与域。

## 目录速查
- `__manifest__.py`：模块元数据/依赖
- `security/*.xml`：访问控制与记录规则
- `views/`：界面、动作、菜单
- `report/`：QWeb 报表与动作
- `static/`：JS/CSS/图片
- `data/`：初始化数据、序列、参数
- `demo/`：演示数据
- `i18n/`：翻译文件（中文术语已统一）

## 调试与运维
- 查看日志：`docker logs -f lookkkedu-odoo`
- 开发者模式：可定位视图/动作/组来源。
- 避免改动 Odoo 核心，修复/自定义优先放本仓库。
- 报表中文文件名异常：升级 `openeducat_core,openeducat_library` 并检查翻译无全角 `%`/括号。
- 翻译未生效：确认系统语言为简体中文，并升级对应模块。

## 路线图（概述）
- 持续优化移动体验、性能、第三方集成，按社区反馈补充模块与 UI/UX。

## 许可证
遵循 **LGPL-3.0**，详见 `LICENSE`。
