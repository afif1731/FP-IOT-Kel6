// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    'nuxt-mapbox'
  ],
  mapbox: {
    accessToken: process.env.MAPBOX_KEY
  },
  css: ["bootstrap/scss/bootstrap.scss"],
  ssr: false,
  vite: {
		resolve: {
			preserveSymlinks: true
		}
	},
  runtimeConfig: {
    public: {
      MQTT_URI: process.env.MQTT_URI,
      WORK_TYPE: process.env.WORK_TYPE,
      MAPBOX_KEY: process.env.MAPBOX_KEY
    }
  }
})
