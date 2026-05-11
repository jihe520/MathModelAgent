<script setup lang="ts">
import {
	BILLBILL,
	DISCORD,
	GITHUB_LINK,
	QQ_GROUP,
	TWITTER,
	XHS,
} from "@/utils/const";
import NavUser from "./NavUser.vue";

import {
	Sidebar,
	SidebarContent,
	SidebarFooter,
	SidebarGroup,
	SidebarGroupContent,
	SidebarGroupLabel,
	SidebarHeader,
	SidebarMenu,
	SidebarMenuButton,
	SidebarMenuItem,
	type SidebarProps,
	SidebarRail,
} from "@/components/ui/sidebar";

// ---- Props ----

const props = defineProps<SidebarProps>();

// ---- Reactive State ----

/** 导航菜单数据 */
const data = {
	navMain: [
		{
			title: "开始",
			url: "#",
			items: [
				{
					title: "开始新任务",
					url: "#",
					isActive: false,
				},
			],
		},
		{
			title: "历史任务",
			url: "#",
			items: [],
		},
	],
};

const socialMedia = [
	{
		name: "QQ",
		url: QQ_GROUP,
		icon: "/qq.svg",
	},
	{
		name: "Twitter",
		url: TWITTER,
		icon: "/twitter.svg",
	},
	{
		name: "GitHub",
		url: GITHUB_LINK,
		icon: "/github.svg",
	},
	{
		name: "哔哩哔哩",
		url: BILLBILL,
		icon: "/bilibili.svg",
	},
	{
		name: "小红书",
		url: XHS,
		icon: "/xiaohongshu.svg",
	},
	{
		name: "Discord",
		url: DISCORD,
		icon: "/discord.svg",
	},
];
</script>

<template>
  <Sidebar v-bind="props">
    <SidebarHeader>
      <!-- 图标 -->
      <div class="flex items-center gap-2 h-15">
        <router-link to="/" class="flex items-center gap-2">
          <img src="@/assets/icon.png" alt="logo" class="w-10 h-10">
          <div class="text-lg font-bold">MathModelAgent</div>
        </router-link>
      </div>
    </SidebarHeader>
    <SidebarContent>
      <SidebarGroup v-for="item in data.navMain" :key="item.title">
        <SidebarGroupLabel>{{ item.title }}</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="childItem in item.items" :key="childItem.title">
              <SidebarMenuButton as-child :is-active="childItem.isActive">
                <a :href="childItem.url">{{ childItem.title }}</a>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
    <SidebarRail />
    <SidebarFooter>
      <NavUser />
    </SidebarFooter>
    <SidebarFooter>
      <!-- 展示图标社交媒体  -->
      <div class="flex items-center gap-4 justify-centermb-4 border-t  border-light-purple pt-3">
        <a v-for="item in socialMedia" :href="item.url" target="_blank">
          <img :src="item.icon" :alt="item.name" width="24" height="24" class="icon">
        </a>
      </div>
    </SidebarFooter>
  </Sidebar>
</template>