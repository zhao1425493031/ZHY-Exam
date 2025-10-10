<template>
  <el-dropdown @command="handleThemeChange" trigger="click">
    <div class="theme-switcher">
      <el-icon size="20"><Brush /></el-icon>
      <span class="theme-name">{{ getCurrentTheme.name }}</span>
      <el-icon size="14"><ArrowDown /></el-icon>
    </div>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item 
          v-for="theme in getAllThemes()" 
          :key="theme.key"
          :command="theme.key"
          :class="{ active: currentTheme === theme.key }"
        >
          <div class="theme-option">
            <div class="theme-preview" :style="{ background: theme.gradient }"></div>
            <span>{{ theme.name }}</span>
            <el-icon v-if="currentTheme === theme.key" size="16"><Check /></el-icon>
          </div>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script>
import { Brush, ArrowDown, Check } from '@element-plus/icons-vue'
import { useTheme } from '@/composables/useTheme'

export default {
  name: 'ThemeSwitcher',
  components: {
    Brush,
    ArrowDown,
    Check
  },
  setup() {
    const { currentTheme, getCurrentTheme, setTheme, getAllThemes } = useTheme()
    
    const handleThemeChange = (themeKey) => {
      setTheme(themeKey)
    }
    
    return {
      currentTheme,
      getCurrentTheme,
      getAllThemes,
      handleThemeChange
    }
  }
}
</script>

<style lang="scss" scoped>
.theme-switcher {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--theme-surface);
  border: 1px solid var(--theme-border);
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: var(--theme-primary);
    color: white;
    border-color: var(--theme-primary);
  }
  
  .theme-name {
    font-size: 14px;
    font-weight: 500;
  }
}

.theme-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
  
  .theme-preview {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid var(--theme-border);
  }
  
  span {
    flex: 1;
    font-size: 14px;
  }
}

:deep(.el-dropdown-menu__item) {
  &.active {
    background: var(--theme-primary);
    color: white;
    
    &:hover {
      background: var(--theme-primary);
    }
  }
}
</style>
