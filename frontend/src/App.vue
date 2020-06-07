<template>
  <v-app>
    <div>
    Lore impsum blablabla.
    Lore impsum blablabla.
    Lore impsum blablabla.
    </div>
    <v-bottom-navigation
        fixed
        position="absolute"
        background-color="#03fcf0"
    >
        <v-spacer>
        </v-spacer>
        <v-bottom-sheet
            v-model="sheet"
        >
            <template v-slot:activator="{ on }">
            <v-btn
                id="cameraBtn"
                fab
                color="#03fcf0"
                v-on:click="cameraMode"
                v-on="on"
            >
                 <v-icon>mdi-camera</v-icon>
            </v-btn>
            </template>
            <v-sheet height="300px">
            <div id="scaleVideo"><video ref="video" id="video" width="1280" height="720" autoplay></video></div>
            <div id="labels" >
                <p>UUID:</p>
                <p>asdfaasdfafasdfasdfsdf</p>
            </div>

            </v-sheet>
        </v-bottom-sheet>
    </v-bottom-navigation>

  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  },
  methods: {
    cameraMode() {
      setTimeout(() => {
        this.video = document.querySelector('#video');
        console.log(this.video);
        if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          navigator.mediaDevices.getUserMedia({ video: { width: { ideal: 1280 }, height: { ideal: 720}}, audio: false }).then(stream => {
            this.video.srcObject = stream;
          });
        }
      }, 300);
    },
  },

data: () => ({
             //
             }),
};
</script>

<style>
#scaleVideo {
  transform-origin: left top;
  transform: scale(calc(300/720));
}
#labels {
  position: absolute;
  margin: 1.5em;
  right: 0;
  top: 0;
}
.v-sheet {
  position: relative;
}




</style>
