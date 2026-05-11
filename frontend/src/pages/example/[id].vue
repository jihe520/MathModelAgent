<script setup lang="ts">
import { Button } from "@/components/ui/button";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import mcmProblemC1 from "@/assets/example/2025-51MCM-Problem C_01.png";
import mcmProblemC2 from "@/assets/example/2025-51MCM-Problem C_02.png";
import huashuCup from "@/assets/example/华数杯2023年C题.png";

// ---- Types ----

/** 图片映射表 */
const imageMap: Record<number, string> = {
	1: huashuCup,
	2: mcmProblemC1,
	3: mcmProblemC2,
};

/** 建模样例数据结构 */
interface ModelingExample {
	id: number;
	title: string;
	source: string;
	description: string;
	tags: string[];
	problemText: string;
	image?: string;
}

// ---- Reactive State ----

const route = useRoute();
const router = useRouter();
const exampleId = route.params.id as string;
const example = ref<ModelingExample | null>(null);
const loading = ref(true);

// ---- Lifecycle Hooks ----

onMounted(() => {
	const storedExample = localStorage.getItem("viewingExample");
	if (storedExample) {
		const parsedExample = JSON.parse(storedExample) as ModelingExample;
		// 确保示例有图片属性，如果没有，从映射中获取
		if (!parsedExample.image && imageMap[parsedExample.id]) {
			parsedExample.image = imageMap[parsedExample.id];
		}
		example.value = parsedExample;
		loading.value = false;
	} else {
		// 如果没有找到缓存的数据，可以模拟一个API请求
		// 实际项目中应该从API获取
		setTimeout(() => {
			const id = Number.parseInt(exampleId);
			example.value = {
				id,
				title: "数学建模样例案例",
				source: "全国大学生数学建模竞赛",
				description: "这是一个示例数模案例。",
				tags: ["数据分析", "算法优化"],
				problemText: "这里是完整的竞赛题目描述文本。",
				image: imageMap[id] || mcmProblemC1,
			};
			loading.value = false;
		}, 800);
	}
});

// ---- Methods ----

/** 基于当前样例开始新任务 */
const startModelingTask = () => {
	if (example.value) {
		localStorage.setItem("selectedExample", JSON.stringify(example.value));
		router.push("/task/create");
	}
};

/** 返回样例列表 */
const goBack = () => {
	router.push("/chat");
};
</script>

<template>
  <div class="container mx-auto py-8 px-4 max-w-4xl">
    <Button variant="ghost" class="mb-6" @click="goBack">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
        <path d="m15 18-6-6 6-6" />
      </svg>
      返回首页
    </Button>

    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full"></div>
    </div>

    <div v-else-if="example" class="space-y-8">
      <div class="space-y-4">
        <h1 class="text-2xl font-semibold">{{ example.title }}</h1>
        <p class="text-muted-foreground">{{ example.source }}</p>
        <div class="flex flex-wrap gap-2 mt-4">
          <span v-for="tag in example.tags" :key="tag"
            class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm">
            {{ tag }}
          </span>
        </div>
      </div>

      <!-- 题目图片 -->
      <div v-if="example.image" class="rounded-lg overflow-hidden border">
        <img :src="example.image" alt="题目图片" class="w-full h-auto" />
      </div>

      <div class="space-y-4">
        <h2 class="text-xl font-medium">题目描述</h2>
        <div class="p-6 border rounded-lg bg-muted/20">
          <p class="whitespace-pre-line">{{ example.problemText }}</p>
        </div>
      </div>

      <div class="space-y-4">
        <h2 class="text-xl font-medium">解题思路</h2>
        <div class="p-6 border rounded-lg">
          <ol class="list-decimal list-inside space-y-3">
            <li>分析问题背景和关键变量</li>
            <li>收集和预处理相关数据</li>
            <li>构建数学模型并确定算法</li>
            <li>实现代码并训练模型</li>
            <li>验证模型并分析结果</li>
            <li>撰写论文并呈现结论</li>
          </ol>
        </div>
      </div>

      <div class="flex justify-center pt-6">
        <Button size="lg" @click="startModelingTask">
          基于此案例开始建模
        </Button>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p>未找到相关样例</p>
      <Button variant="outline" class="mt-4" @click="goBack">返回首页</Button>
    </div>
  </div>
</template>