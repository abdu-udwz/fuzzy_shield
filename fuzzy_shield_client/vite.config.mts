// Plugins
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import Fonts from 'unplugin-fonts/vite'
import Layouts from 'vite-plugin-vue-layouts'
import Vue from '@vitejs/plugin-vue'
import VueRouter from 'unplugin-vue-router/vite'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { ConfigEnv, defineConfig, loadEnv} from 'vite'
import { fileURLToPath, URL } from 'node:url'
import path from 'node:path'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  const serverBaseURL = createServerConfig({ command, mode })

  return {
  plugins: [
    VueRouter({
      dts: 'src/typed-router.d.ts',
    }),
    Layouts(),
    AutoImport({
      imports: [
        'vue',
        {
          'vue-router/auto': ['useRoute', 'useRouter'],
        }
      ],
      dts: 'src/auto-imports.d.ts',
      eslintrc: {
        enabled: true,
      },
      vueTemplate: true,
    }),
    Components({
      dts: 'src/components.d.ts',
    }),
    Vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify({
      autoImport: true,
    }),
    Fonts({
      google: {
        families: [ {
          name: 'Roboto',
          styles: 'wght@100;300;400;500;700;900',
        }],
      },
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: serverBaseURL,
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: "../fuzzy_shield/public",
    emptyOutDir: true,
  },
  base: '/app/'
}
})


function createServerConfig({ command, mode }: ConfigEnv) {
  let { SERVER_HOST, SERVER_BASE_PATH, SERVER_API_PATH } = loadEnv(mode, process.cwd(), '')

  // == dev serve proxy-ing config
  let relativeToServerPath = ''
  let serverBaseURL = ''
  let serverApiURL = ''
  if (command === 'serve') {
    if (SERVER_HOST == null) {
      SERVER_HOST = 'http://localhost:3000'
    }

    if (SERVER_BASE_PATH == null) {
      SERVER_BASE_PATH = '/'
    }

    if (SERVER_API_PATH == null) {
      SERVER_API_PATH = '/'
    }

    // prepare server urls
    relativeToServerPath = path.join(SERVER_BASE_PATH, SERVER_API_PATH)
    serverBaseURL = new URL(SERVER_BASE_PATH, SERVER_HOST).href
    serverApiURL = new URL(relativeToServerPath, SERVER_HOST).href

    console.log('[DEV API] Using server at', serverBaseURL, 'as API server')
    console.log('[DEV API] Full API target is:', serverApiURL)
  }
  return serverBaseURL
}
