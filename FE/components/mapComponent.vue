<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import 'mapbox-gl/dist/mapbox-gl.css';
import mapboxgl from 'mapbox-gl';

const props = defineProps<{
  center: [mapboxgl.LngLat.lng, mapboxgl.LngLat.lat];
}>();
const mapContainer = ref<HTMLElement | null>(null);
const map = ref<mapboxgl.Map | null>(null);

const config = useRuntimeConfig();
const mapboxAccessToken = config.public.MAPBOX_KEY;

onMounted(() => {
mapboxgl.accessToken = mapboxAccessToken;

map.value = new mapboxgl.Map({
    container: mapContainer.value!,
    style: 'mapbox://styles/mapbox/streets-v12',
    center: props.center as [mapboxgl.LngLat.lng, mapboxgl.LngLat.lat], // Menggunakan center dari props
    zoom: 16
});

new mapboxgl.Marker()
    .setLngLat(props.center as [mapboxgl.LngLat.lng, mapboxgl.LngLat.lat])
    .setPopup(new mapboxgl.Popup({ offset: 0 }).setText('Box Position'))
    .addTo(map.value);
});

// Watcher untuk mengamati perubahan center dan meng-update peta
// watch(
//   () => props.center,
//   (newCenter) => {
//     if (map.value) {
//     map.value.setCenter(newCenter as [number, number]);
//     }
//   }
// );
</script>

<style scoped>
.map-container {
    width: 100%;
    height: 50vh;
}
</style>
  