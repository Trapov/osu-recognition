import UserCard from "./components/userCard.js";

const availablePages = {
  USERS: 'users',
  AUTH: 'auth',
  OPTIONS: 'options'
}

const vue = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {
      UserCard
  },
  data() {
    return {
      adminToken: '',
      loading: false,
      currentPage: availablePages.AUTH,
      settingsPage : {
        count: 8,
        offset: 0,
        total: 0,
        items: []
      },
      settings: {
        loading: false,
        valid: true,
        name: '',
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
      usersPage: {
        count: 8,
        offset: 0,
        total: 0,
        items: []
      },
    }
  },
  methods: {
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
          console.error(result);
        }
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