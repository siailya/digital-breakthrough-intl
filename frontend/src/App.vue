<template>
  <n-config-provider
      :date-locale="dateRuRU"
      :locale="ruRU"
      :theme="lightTheme"
      :theme-overrides="themeOverrides"
  >
    <n-dialog-provider>
      <n-message-provider>
        <n-layout style="height: 100vh;">
          <n-layout-header bordered style="padding: 10px 20px">
            <div style="display:flex;">
              <div class="logo-wrapper">
                <img src="@/assets/images/publicpulse_logo.svg" width="300" class="logo-md" alt="">
                <img src="@/assets/images/publicpulse_icon.svg" width="70" class="logo-sm" alt="">
              </div>

              <n-space style="margin: auto 0 auto 24px;">
                <n-button text @click="$router.push('/classification')"
                          :class="$route.path === '/classification' && 'active'">
                  Классификация комментариев
                </n-button>
                <n-button text @click="$router.push('/package')" :class="$route.path === '/package' && 'active'">
                  Пакетная обработка
                </n-button>
              </n-space>

              <div style="margin: auto 12px auto auto; display:flex; gap: 16px">
                <n-button @click="onClickOpenSettingsModal">
                  Настройки
                </n-button>

                <n-modal :show="isSettingsModalOpen" close-on-esc closable>
                  <n-card style="max-width: 576px" title="Настройки" closable @close="isSettingsModalOpen = false">
                    <n-form-item label="API URL">
                      <n-input v-model:value="rootStore.apiUrl"/>
                    </n-form-item>

                    <n-button @click="isSettingsModalOpen = false" block type="primary">
                      Сохранить и закрыть
                    </n-button>
                  </n-card>
                </n-modal>
                <img alt="" src="@/assets/images/flint3s_logo.png" style="width: 80px">
              </div>
            </div>
          </n-layout-header>

          <n-layout-content content-style="padding: 20px">
            <router-view v-slot="{ Component }">
              <transition mode="out-in" name="fade">
                <component :is="Component"/>
              </transition>
            </router-view>
          </n-layout-content>
        </n-layout>
      </n-message-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>

<script lang="ts" setup>
import {
  dateRuRU,
  lightTheme,
  NButton,
  NCard,
  NConfigProvider,
  NDialogProvider,
  NFormItem,
  NInput,
  NLayout,
  NLayoutContent,
  NLayoutHeader,
  NMessageProvider,
  NModal,
  NSpace,
  ruRU
} from "naive-ui";
import themeOverrides from "@/assets/style/naive-ui-theme-overrides.json";
import {ref} from "vue";
import {useRootStore} from "@/stores/root";

const isSettingsModalOpen = ref(false);
const rootStore = useRootStore()

const onClickOpenSettingsModal = () => {
  isSettingsModalOpen.value = true
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
}

#app {
  height: 100vh;
}

.content-padding {
  padding: 20px;
}

.active {
  color: #CB4302;
}

.container-md {
  max-width: 768px;
  margin: 0 auto;
}

.logo-wrapper img {
  display: none;
}

@media screen and (max-width: 768px) {
  .logo-wrapper .logo-sm {
    display: block;
  }
}

@media screen and (min-width: 768px) {
  .logo-wrapper .logo-md {
    display: block;
  }
}
</style>