<template>
  <main class="container-md">
    <n-h2 style="font-weight: normal">Пакетная классификация</n-h2>

    <n-form-item label="Тексты обращений" feedback="Тексты обращений, каждое новое обращение на отдельной строке">
      <n-input type="textarea" placeholder="Текст обращений"
               :loading="isLoading" v-model:value="requestsText"/>
    </n-form-item>

    <div style="text-align: center; margin: 6px">- или -</div>

    <n-upload accept=".txt" style="width: 100%" trigger-style="width: 100%" @change="onSelectFile" ref="uploader"
              :file-list="selectedFiles">
      <n-button block secondary type="primary">
        Загрузить файл
      </n-button>
    </n-upload>

    <n-divider/>

    <n-button type="primary" block :loading="isLoading" @click="onClickSentToClassify">
      Классифицировать обращения
    </n-button>

    <n-h2 style="font-weight: normal">Результаты классификации</n-h2>
    <n-spin v-if="isLoading">
    </n-spin>
    <n-h3 v-else-if="!classificationResults.isClassified">Введите текст обращения и отправьте его на классификацию для
      получения результата
    </n-h3>
    <n-collapse vertical v-else>
      <n-collapse-item v-for="classificationItem in classificationResults.results"
                       :title="classificationItem.originalText.substring(0, 50) + '...'">
        <n-space vertical>
          <div>
            <n-h3>
              Текст обращения:
              <br>
              <span style="font-weight: normal; font-size: 14px">{{ classificationItem.originalText }}</span>
            </n-h3>
          </div>
          <n-h3 style="font-weight: normal; margin-bottom: 6px;">
            <span style="font-weight: 500">Группа тем:</span>
            {{ classificationItem.themesGroup }}
          </n-h3>
          <n-h3 style="font-weight: normal; margin-bottom: 6px;">
            <span style="font-weight: 500">Тема:</span>
            {{ classificationItem.theme }}
          </n-h3>
          <n-h3 style="font-weight: normal; margin-bottom: 6px;">
            <span style="font-weight: 500">Исполнитель:</span>
            {{ classificationItem.assignee }}
          </n-h3>
        </n-space>
      </n-collapse-item>
    </n-collapse>
  </main>
</template>

<script setup lang="ts">
import {
  NButton,
  NCollapse,
  NCollapseItem,
  NDivider,
  NFormItem,
  NH2,
  NH3,
  NInput,
  NSpace,
  NSpin,
  NUpload,
  type UploadFileInfo
} from "naive-ui"
import {reactive, ref} from "vue";
import axios from "axios";
import {useRootStore} from "@/stores/root";

const isLoading = ref(false);
const uploader = ref<any>(null);
const selectedFiles = ref<UploadFileInfo[]>([]);
const requestsText = ref('');
const rootStore = useRootStore()

const classificationResults = reactive<{
  isClassified: boolean, results: {
    originalText: string,
    theme: string,
    themesGroup: string,
    assignee: string,
  }[]
}>({
  isClassified: false,
  results: []
})

const onSelectFile = (e: { file?: UploadFileInfo, fileList: any[] }) => {
  selectedFiles.value = e.fileList.length ? [e.file!] : [];
  e.file!.file?.text().then(text => {
    requestsText.value = text
    selectedFiles.value = [];
  });
}

const onClickSentToClassify = () => {
  classificationResults.isClassified = false;
  classificationResults.results = [];

  const lines = requestsText.value.split('\n').map(s => s.trim()).filter(s => s.length > 0);
  for (let i = 0; i < lines.length; i += 15) {
    const chunk = lines.slice(i, i + 15);
    axios.post(`${rootStore.apiUrl}/classify_package`, {
      texts: chunk
    })
        .then(response => {
          classificationResults.isClassified = true;
          classificationResults.results.push(...response.data as any);
        })
  }
}
</script>
