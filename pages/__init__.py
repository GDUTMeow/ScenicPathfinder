from streamlit import Page

HOME_PAGE = Page("pages/home.py", title="首页")

GUEST_FIND_SPOT_PAGE = Page("pages/guest/find_spot.py", title="查询景点")
GUEST_FIND_SHORTEST_PATH_PAGE = Page(
    "pages/guest/find_shortest_path.py", title="查询最短路径"
)
GUEST_FIND_ALL_SIMPLE_PATH_PAGE = Page(
    "pages/guest/find_all_simple_path.py", title="查询所有简单路径"
)
GUEST_GET_PLAN_PAGE = Page("pages/guest/get_plan.py", title="游览路线规划")
GUEST_VIEW_MAP_PAGE = Page("pages/guest/view_map.py", title="景区地图")

ADMIN_ADD_SPOT_PAGE = Page("pages/admin/add_spot.py", title="添加景点")
ADMIN_REMOVE_SPOT_PAGE = Page("pages/admin/remove_spot.py", title="删除景点")
ADMIN_MODIFY_SPOT_PAGE = Page("pages/admin/modify_spot.py", title="修改景点")
ADMIN_ADD_PATH_PAGE = Page("pages/admin/add_path.py", title="添加道路")
ADMIN_MODIFY_PATH_PAGE = Page("pages/admin/modify_path.py", title="修改道路")
ADMIN_REMOVE_PATH_PAGE = Page("pages/admin/remove_path.py", title="删除道路")

DEBUG_DATA_VIEW_PAGE = Page("pages/debug/data_view.py", title="数据查看")
DEBUG_GENERATE_DATA_PAGE = Page("pages/debug/generate_data.py", title="生成测试数据")
