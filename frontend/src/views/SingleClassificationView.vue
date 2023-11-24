<template>
  <main class="container-md">
    <n-h2 style="font-weight: normal">Классификация обращения</n-h2>

    <n-form-item label="Текст обращения">
      <n-input type="textarea" placeholder="Текст обращения" :loading="isLoading"/>
    </n-form-item>

    <n-button type="primary" block :loading="isLoading" @click="onClickSentToClassify">
      Классифицировать обращение
    </n-button>

    <n-h2 style="font-weight: normal">Результаты классификации</n-h2>
    <n-spin v-if="isLoading">
    </n-spin>
    <n-h3 v-else-if="!classificationResult.isClassified">Введите текст обращения и отправьте его на классификацию для получения результата</n-h3>
    <n-space vertical v-else>
      <n-h3 style="font-weight: normal; margin-bottom: 6px;">
        <span style="font-weight: 500">Группа тем:</span>
        {{classificationResult.themesGroup}}
      </n-h3>
      <n-h3 style="font-weight: normal; margin-bottom: 6px;">
        <span style="font-weight: 500">Тема:</span>
        {{classificationResult.theme}}
      </n-h3>
      <n-h3 style="font-weight: normal; margin-bottom: 6px;">
        <span style="font-weight: 500">Исполнитель:</span>
        {{classificationResult.assignee}}
      </n-h3>
    </n-space>
  </main>
</template>

<script setup lang="ts">
import {NFormItem, NH2, NH3, NInput, NButton, NSpace, NSpin} from "naive-ui"
import {reactive, ref} from "vue";
import axios from "axios";

const isLoading = ref(false);
const classificationResult = reactive({
  isClassified: false,
  themesGroup: "",
  theme: "",
  assignee: "",
})

const clearClassificationResult = () => {
  classificationResult.isClassified = false;
  classificationResult.themesGroup = "";
  classificationResult.theme = "";
  classificationResult.assignee = "";
}

const onClickSentToClassify = () => {
  clearClassificationResult();
  isLoading.value = true;

  axios.get("https://run.mocky.io/v3/4cc59900-0ca5-442a-9438-e53771a84691")
    .then(res => {
      classificationResult.isClassified = true;
      classificationResult.themesGroup = res.data.themesGroup;
      classificationResult.theme = res.data.theme;
      classificationResult.assignee = res.data.assignee;
    })
   .catch(err => {
      console.log(err);
    })
   .finally(() => {
      isLoading.value = false;
    });
}
</script>
