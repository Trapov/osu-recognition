import UserCard from "./components/userCard.js";
import VueJsonPretty from "./components/vue-pretty-print/index.js";

const availablePages = {
  USERS: 'users',
  AUTH: 'auth',
  LOGS: 'logs',
  OPTIONS: 'options'
}
        
Date.prototype.addHours = function(h) {
  this.setTime(this.getTime() + (h*60*60*1000));
  return this;
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {

  options = {
    path: '/admin',
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}
const vue = new Vue({
  el: '#app',
  vuetify: new Vuetify({
    theme: {
      dark : true
    }
  }),
  components: {
      UserCard,
      VueJsonPretty
  },
  data() {
    return {
      logs: [],
      showPassword: false,
      providedAdminToken: '',
      loading: false,
      currentPage: availablePages.AUTH,
      logsFilter : {
        warn: true,
        info: true,
        error: true
      },
      settingsPage : {
        count: 2,
        offset: 0,
        total: 0,
        items: []
      },
      settings: {
        loading: false,
        valid: true,
        name: '',
        storage_backend: 'sqlite',
        is_active : '',
        max_features : '',
        base_threshold : '',
        rate_of_decreasing_threshold_with_each_feature: '',
        created_at : '',
        updated_at: '',
        resize_factors: {
          x : '',
          y: ''
        }
      },
      metrics: {
        loading: false,
      },
      usersPage: {
        count: 8,
        offset: 0,
        total: 0,
        items: []
      },
    }
  },
  computed: {
    logsFiltered() {
      let filteredValue = this.logs;
      if (this.logsFilter.info == false) {
        filteredValue = filteredValue.filter(l => l.levelname != "INFO");
      }

      if (this.logsFilter.warn == false) {
        filteredValue = filteredValue.filter(l => l.levelname != "WARN");
      }

      if (this.logsFilter.error == false) {
        filteredValue = filteredValue.filter(l => l.levelname != "ERROR");
      }

      return filteredValue;
    },
    adminToken : {
      get: function() {
        return this.providedAdminToken || (this.providedAdminToken = getCookie('adminToken'));
      },
      set: function(newValue) {
        this.providedAdminToken = newValue;
      }
    }
  },
  methods: {
    setAdminToken (newValue) {
      setCookie('adminToken', newValue, {expires: new Date().addHours(2) });
    },

    onUserDeleted(id) {
      this.usersPage.items = this.usersPage.items.filter(i => i.id !== id);
    },

    async refreshPage(){
      try{
        this.loading = true;
        const result = await fetch(`/users?offset=${this.usersPage.offset}&count=${this.usersPage.count}`, { 
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const page = await result.json();
        this.usersPage.total = page.total;
        this.usersPage.items = page.values;
      }
      finally{
        this.loading = false;
      }
    },
    async getMetrics() {
      try{
        this.loading = true;
        this.metrics.loading = true;
        const result = await fetch(`/metrics`, { 
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const metrics = await result.json();
        Object.assign(this.metrics, metrics);
      }
      finally{
        this.metrics.loading = false;
        this.loading = false;
      }
    },
    async getCurrentSettings(){
      try{
        this.loading = true;
        this.settings.loading = true;
        const result = await fetch(`/settings/current`, { 
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const settings = await result.json();
        Object.assign(this.settings, settings);
      }
      finally{
        this.settings.loading = false;
        this.loading = false;
      }
    },

    async saveSettings(settings){
      try{
        this.loading = true;
        this.settings.loading = true;
        const result = await fetch(`/settings`, { 
          method: 'POST',
          headers: {
            'Content-Type' : 'application/json',
            'Authorization': `Bearer ${this.adminToken}`
          },
          body: JSON.stringify(settings)
        });
        if(result.status != 201){
          console.error('Could not save the settings', result);
        }
        await this.goToOptions();
      }
      finally{
        this.settings.loading = false;
        this.loading = false;
      }
    },

    async getSettings(){
      try{
        this.loading = true;
        this.settings.loading = true;
        const result = await fetch(`/settings?offset=${this.settingsPage.offset}&count=${this.settingsPage.count}`, { 
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const settings = await result.json();
        settings.values = settings.values.filter(v => v.is_active == false);
        this.settingsPage.total = settings.total;
        this.settingsPage.items = settings.values;
      }
      finally{
        this.settings.loading = false;
        this.loading = false;
      }
    },

    
    async getLastLogs(){
      try{
        this.loading = true;
        const result = await fetch(`/logs`, { 
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        this.logs = await result.json();

      }
      finally{
        this.loading = false;
      }
    },

    canGoBack() {
      return this.usersPage.offset != 0;
    },
    canGoForward() { 
      return this.usersPage.count < (this.usersPage.total - this.usersPage.offset);
    },

    canGoBackSettings() {
      return this.settingsPage.offset != 0;
    },
    canGoForwardSettings() { 
      return this.settingsPage.count < (this.settingsPage.total - this.settingsPage.offset);
    },


    async goToOptions(){
      await this.getCurrentSettings();
      await this.getSettings();
      this.currentPage = availablePages.OPTIONS
    },

    async goToLogs(){
      await this.getLastLogs();
      const refThis = this;
      await refThis.getMetrics()
      setInterval(async function() {
        await refThis.getMetrics()
      }, 60000)
      this.currentPage = availablePages.LOGS
    },

    async goToUsers(){
      await this.refreshPage();
      this.currentPage = availablePages.USERS
    },

    async goForwardSettings(){
      try{
        if(!this.canGoForwardSettings()){
          return;
        }
        const newOffset = this.settingsPage.offset + this.settingsPage.count;
        this.loading = true;
        const result = await fetch(`/settings?offset=${newOffset}&count=${this.settingsPage.count}`, { 
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const page = await result.json();
        this.settingsPage.offset = newOffset;
        this.settingsPage.total = page.total;
        this.settingsPage.items = page.values;
      }
      catch(exception){
        console.error(exception)
      }
      finally{
        this.loading = false;
      }
    },

    async pickNewSettings(settings) {
      settings.is_active = true;
      await this.saveSettings(settings);
    },

    async goBackSettings(){
      try{
        if(!this.canGoBackSettings()){
          return;
        }
        const newOffset = this.settingsPage.offset - this.settingsPage.count;

        this.loading = true;
        const result = await fetch(`/settings?offset=${newOffset}&count=${this.settingsPage.count}`, { 
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const page = await result.json();

        this.settingsPage.offset = newOffset;
        this.settingsPage.total = page.total;
        this.settingsPage.items = page.values;
      }
      catch(exception){
        console.error(exception)
      }
      finally{
        this.loading = false;
      }
    },

    async goForward(){
      try{
        if(!this.canGoForward()){
          return;
        }
        const newOffset = this.usersPage.offset + this.usersPage.count;
        this.loading = true;
        const result = await fetch(`/users?offset=${newOffset}&count=${this.usersPage.count}`, { 
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const page = await result.json();
        this.usersPage.offset = newOffset;
        this.usersPage.total = page.total;
        this.usersPage.items = page.values;
      }
      catch(exception){
        console.error(exception)
      }
      finally{
        this.loading = false;
      }
    },

    async goBack(){
      try{
        if(!this.canGoBack()){
          return;
        }
        const newOffset = this.usersPage.offset - this.usersPage.count;

        this.loading = true;
        const result = await fetch(`/users?offset=${newOffset}&count=${this.usersPage.count}`, { 
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.adminToken}`
          }
        });
        const page = await result.json();

        this.usersPage.offset = newOffset;
        this.usersPage.total = page.total;
        this.usersPage.items = page.values;
      }
      catch(exception){
        console.error(exception)
      }
      finally{
        this.loading = false;
      }
    },

  },
  async mounted() {
    if (this.adminToken){
      await this.refreshPage();
    }
  },
})