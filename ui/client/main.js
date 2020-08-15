import WebCam from './components/webCam.js';
import UserCard from './components/userCard.js';

new Vue({
    el: '#app',
    components: {
        WebCam,
        UserCard
    },
    data() {
      return {
        token: null,
        user: null,
        loading: false
      }
    },
    methods: {
      async loadMe(token){
        try{
          this.loading = true;
          const result = await fetch('/me', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          this.user = await result.json();
        }
        finally{
          this.loading = false;
        }
      }
    },
    watch: {
      async token(newValue, oldValue){
        await this.loadMe(newValue);
      }
    },
    vuetify: new Vuetify({
      theme: {
        dark : true
      }
    }),
})