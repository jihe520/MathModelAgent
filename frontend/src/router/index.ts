import { createRouter, createWebHistory } from "vue-router";

/** 路由配置 */
const routes = [
	{
		path: "/",
		component: () => import("@/pages/index.vue"),
	},
	{
		path: "/login",
		component: () => import("@/pages/login/index.vue"),
	},
	{
		path: "/chat",
		component: () => import("@/pages/chat/index.vue"),
	},
	{
		path: "/task/:task_id",
		component: () => import("@/pages/task/index.vue"),
		props: true,
	},
];

/** 创建路由实例 */
const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
