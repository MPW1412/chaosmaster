<template>
  <v-app>
    <router-view>
      <ImagesComponent/>
    </router-view>
  </v-app>
</template>

<script>
import ImagesComponent from './components/Images';
export default {
  name: 'App',

  components: {
    ImagesComponent
  },

  data(){
    return { 

    }
  },
  methods: {    
  },

           
};
</script>

<style>

</style>
