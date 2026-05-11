<script lang="ts">
export const description = "A login page with form and image.";
</script>

<script setup lang="ts">
import LoginForm from '@/components/LoginForm.vue'
import { GalleryVerticalEnd } from 'lucide-vue-next'
</script>

<template>
  <div class="flex min-h-svh flex-col items-center justify-center bg-muted p-6 md:p-10">
    <a href="#" class="flex items-center gap-2 self-center font-medium mb-8">
      <div class="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
        <GalleryVerticalEnd class="size-4" />
      </div>
      Acme Inc.
    </a>
    <div class="w-full max-w-sm md:max-w-3xl">
      <LoginForm />
    </div>
  </div>
</template>
