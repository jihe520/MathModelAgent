<template>
  <div class="home">
    <button @click="add_md">添加</button>
    <button @click="prevPage">上一页</button>
    <button @click="nextPage">下一页</button>
    <RenderJupyterNotebook :notebook="{ ...notebook, cells: visibleCells }" />
  </div>
</template>

<script setup lang="ts">
import example from "@/assets/jupyter.json";
import RenderJupyterNotebook from "render-jupyter-notebook-vue";
import { computed, ref } from "vue";

const add_content = {
	cell_type: "markdown",
	metadata: {},
	source: [
		"Compared to a table in a Markdown cell:\n",
		"\n",
		"\n",
		'<table style="width:100%">\n',
		"    <thead>\n",
		"  <tr>\n",
		"    <th>Firstname</th>\n",
		"    <th>Lastname</th> \n",
		"    <th>Age</th>\n",
		"  </tr>\n",
		"  </thead>\n",
		"  <tr>\n",
		"    <td>Jill</td>\n",
		"    <td>Smith</td> \n",
		"    <td>50</td>\n",
		"  </tr>\n",
		"  <tr>\n",
		"    <td>Eve</td>\n",
		"    <td>Jackson</td> \n",
		"    <td>94</td>\n",
		"  </tr>\n",
		"</table>",
	],
};

const notebook = ref(JSON.parse(JSON.stringify(example))); // 深拷贝原始数据

// 添加分页相关状态
const pageSize = ref(10); // 每页显示的数量
const currentPage = ref(1);

// 计算当前页要显示的内容
const visibleCells = computed(() => {
	const start = (currentPage.value - 1) * pageSize.value;
	const end = start + pageSize.value;
	return notebook.value.cells.slice(start, end);
});

const add_md = () => {
	notebook.value.cells = [add_content, ...notebook.value.cells]; // 使用展开运算符添加新内容
	console.log("add_md");
	console.log(notebook.value);
	currentPage.value = 1; // 添加新内容后回到第一页
};

// 分页控制
const nextPage = () => {
	if (currentPage.value * pageSize.value < notebook.value.cells.length) {
		currentPage.value++;
	}
};

const prevPage = () => {
	if (currentPage.value > 1) {
		currentPage.value--;
	}
};
</script>