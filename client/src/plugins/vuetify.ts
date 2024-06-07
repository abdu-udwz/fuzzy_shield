/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import 'vuetify/styles'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  defaults: {
    global: {
      density: 'default'
    },
    VInput: {
      variant: 'filled',
      flat: true
    },
    VTextField: {
      variant: 'filled',
      flat: true
    },
    VCombobox: {
      variant: 'filled',
      flat: true
    },
    VSelect: {
      variant: 'filled',
      flat: true
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'dark',
  },
})
