module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/standard'
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'off',
    'no-unused-vars': 'off',
    'space-before-function-paren': 'off',
    'comma-dangle': 'off',
    'semi': 'off',
    'quotes': 'off',
    'indent': 'off',
    'no-trailing-spaces': 'off',
    'vue/no-reserved-component-names': 'off',
    'camelcase': 'off',
    'no-dupe-keys': 'off',
    'operator-linebreak': 'off',
    'multiline-ternary': 'off',
    'no-case-declarations': 'off',
    'no-prototype-builtins': 'off',
    'no-return-assign': 'off',
    'no-multiple-empty-lines': 'off',
    'quote-props': 'off',
    'no-undef': 'off',
    'eol-last': 'off',
    'vue/no-dupe-keys': 'off'
  },
  globals: {
    defineProps: 'readonly',
    defineEmits: 'readonly',
    defineExpose: 'readonly',
    withDefaults: 'readonly'
  }
}
