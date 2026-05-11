<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
	Dialog,
	DialogClose,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
} from "@/components/ui/dialog";

const modelValue = defineModel({
	type: Boolean,
	default: false,
});
</script>

<template>
  <Dialog :open="modelValue" @update:open="modelValue = false">
    <DialogContent>

      <DialogHeader>
        <DialogTitle>更多</DialogTitle>
        <DialogDescription>
          更多信息
        </DialogDescription>
      </DialogHeader>
      <div>
        运行的结果:
        backend/project/work_dir/xxx/*
        <br>
        - notebook.ipynb: 保存运行过程中产生的代码<br>

        - res.md: 保存最后运行产生的结果为 markdown 格式
      </div>

      <div>
        修改模板：
        backend/app/config/md_template.toml
      </div>

      <div>
        修改提示词
        backend/app/core/prompts.py
      </div>

    </DialogContent>
  </Dialog>
</template>
