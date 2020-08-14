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

    canGoBack() {
      return this.usersPage.offset != 0;
    },
    canGoForward() { 
      return this.usersPage.count < (this.usersPage.total - this.usersPage.offset);
    },

    canGoBackSettings() {
      return this.usersPage.offset != 0;
    },
    canGoForwardSettings() { 
      return this.usersPage.count < (this.usersPage.total - this.usersPage.offset);
    },


    async goToOptions(){
      await this.getCurrentSettings();
      this.currentPage = availablePages.OPTIONS
    },

    async goToUsers(){
      await this.refreshPage();
      this.currentPage = availablePages.USERS
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