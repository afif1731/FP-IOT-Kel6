<template>
    <body>
        <div class=" mb-4 homeheader">
            <div class=" container pt-3">
                <div class=" row">
                    <div class=" col-4">
                        <NuxtLink to="/" class=" text-decoration-none back-btn"><h3>BACK</h3></NuxtLink>
                    </div>
                </div>
                <div class=" row mt-5">
                    <div class=" col greet-text d-flex align-items-center justify-content-center">
                        <h1 class=" text-center">Check Box Condition</h1>
                    </div>
                </div>
            </div>
        </div>

        <div class=" container">
            <div class=" row">
                <div class=" col-6 map-col box-map">
                    <h1>Location: </h1>
                    <mapComponent :center="center" />
                </div>
                <div class=" col-4 offset-2">
                    <h1>Condition: </h1>
                    <div class=" container mt-5">
                        <div class=" row justify-content-center mt-3">
                            <div class=" col-12 align-items-center d-flex px-5 mb-4 justify-content-between box-status">
                                <div><h4>Vibration Detect</h4></div>
                                <div class=" status-text status-safe" v-if="vib_stat == true"><h2> SAFE </h2></div>
                                <div class=" status-text status-alert" v-else><h2> ALERT </h2></div>
                            </div>
                            <div class=" col-12 align-items-center d-flex px-5 mb-4 justify-content-between box-status">
                                <div><h4>Movement Detect</h4></div>
                                <div class=" status-text status-safe" v-if="pir_stat == true"><h2> SAFE </h2></div>
                                <div class=" status-text status-alert" v-else><h2> ALERT </h2></div>
                            </div>

                            <NuxtLink :to="'/secretbox/' + route.params.box_id + '/changepass'" class=" col-12 align-items-center d-flex px-5 mt-5 mb-3 justify-content-between box-btn">
                                <div><h4>Change Password</h4></div>
                                <div><h1> 》 </h1></div>
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script lang="ts" setup>
import { ref, reactive, onBeforeUnmount, onMounted } from 'vue';
import mqtt from 'mqtt';
import { useRoute } from 'vue-router';

interface MqttMessage {
  flag?: string;
  pir?: string;
  vibration?: string;
  [key: string]: any;
}

interface Coordinates {
  long: number;
  lat: number;
}

const config = useRuntimeConfig();

const brokerUrl = config.public.MQTT_URI;
let mqttTopic = '/iot06/box/';
// Reactive state
const mqttClient = ref<mqtt.MqttClient | null>(null);
const mqttMessage = reactive<MqttMessage>({});
const keepAliveInterval = ref<number | null>(null);
const keepAliveTimeout = 60000;
const vib_stat = ref(false);
const pir_stat = ref(false);
const box_coor = reactive<Coordinates>({
  long: 0.0,
  lat: 0.0,
});
const user_coor = reactive<Coordinates>({
  long: 0.0,
  lat: 0.0,
});
const center = ref<[number, number]>([112.79491929114965, -7.282330692448325]);
const isDev = process.env.WORK_TYPE;

// Route info
const route = useRoute();
mqttTopic = `/iot06/box/${route.params.box_id}/pub-sensor`;

function dummyData(): void {
  box_coor.long = 112.79491929114965;
  box_coor.lat = -7.282330692448325;

  user_coor.long = 112.79491929114965;
  user_coor.lat = -7.282330692448325;

  center.value = [box_coor.long, box_coor.lat];
}

function connectToMqtt(): void {
  mqttClient.value = mqtt.connect(brokerUrl as string);

  mqttClient.value.on('connect', () => {
    console.log('Connected to MQTT broker');
    mqttClient.value!.subscribe(mqttTopic, (err) => {
      if (!err) {
        console.log(`Subscribed to topic: ${mqttTopic}`);
        startKeepAlive();
      }
    });
  });

  mqttClient.value.on('message', (topic, message) => {
    if (topic === mqttTopic) {
      try {
        Object.assign(mqttMessage, JSON.parse(message.toString()));

        if (mqttMessage.flag === 'OK') {
          sendMqttMessage();
        }

        pir_stat.value = mqttMessage.pir === 'Freeze';
        vib_stat.value = mqttMessage.vibration === 'Idle';
      } catch (error) {
        console.error('Failed to parse message:', error);
      }
    }
  });

  mqttClient.value.on('close', () => {
    console.log('Connection closed. Attempting to reconnect...');
    stopKeepAlive();
    setTimeout(connectToMqtt, 5000); // Attempt to reconnect after 5 seconds
  });
}

function startKeepAlive(): void {
  if (keepAliveInterval.value !== null) {
    clearInterval(keepAliveInterval.value);
  }
  keepAliveInterval.value = window.setInterval(() => {
    console.log('Sending keep-alive ping');
    mqttClient.value!.publish(mqttTopic, JSON.stringify({ type: 'ping' }));
  }, keepAliveTimeout);
}

function stopKeepAlive(): void {
  if (keepAliveInterval.value !== null) {
    clearInterval(keepAliveInterval.value);
    keepAliveInterval.value = null;
  }
}

function sendMqttMessage(): void {
  const message = {
    response: 'Message received with OK flag',
  };

  const messageString = JSON.stringify(message);
  mqttClient.value!.publish(mqttTopic, messageString, () => {
    console.log('Sent message:', messageString);
  });
}

// Lifecycle hooks
onMounted(() => {
  if (isDev == 'dev') {
    dummyData();
  }
  connectToMqtt();
});

onBeforeUnmount(() => {
  stopKeepAlive();
  if (mqttClient.value) {
    mqttClient.value.end();
  }
});
</script>


<style scoped>
body {
    padding: 0;
    margin: 0;
}

.homeheader {
    background: rgb(25,55,254);
    background: linear-gradient(0deg, rgba(25,55,254,1) 0%, rgba(51,77,251,1) 42%, rgba(73,96,249,1) 100%);
    height: 35vh;
    margin-top: -40px;
    padding-top: 50px;
    border-radius: 50px;
}

.greet-text h1 {
    font-family: monospace;
    color: whitesmoke;
}

.back-btn {
    color: white;
}

.box-status {
    background: rgb(227, 227, 227);
    border-radius: 40px;
    color: rgb(70, 70, 70);
    height: 10vh;
    text-decoration: none;
}

.box-btn {
    background: rgb(73,96,249);
    background: linear-gradient(90deg, rgba(73,96,249,1) 0%, rgba(47,74,252,1) 20%, rgba(20,51,255,1) 100%);
    border-radius: 40px;
    color: white;
    height: 10vh;
    text-decoration: none;
}

.status-safe {
    color: #56F08A;
}

.status-alert {
    color: #f44141;
}

</style>