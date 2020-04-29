import UserCard from "./components/userCard.js";

const vue = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {
      UserCard
  },
  data() {
    return {
      loading: false,
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
        const result = await fetch(`/users?offset=${this.usersPage.offset}&count=${this.usersPage.count}`);
        const page = await result.json();
        this.usersPage.total = page.total;
        this.usersPage.items = page.values;
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

    async goForward(){
      try{
        if(!this.canGoForward()){
          return;
        }
        const newOffset = this.usersPage.offset + this.usersPage.count;
        this.loading = true;
        const result = await fetch(`/users?offset=${newOffset}&count=${this.usersPage.count}`);
        const page = await result.json();
        // console.debug(page);
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
        const result = await fetch(`/users?offset=${newOffset}&count=${this.usersPage.count}`);
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
      await this.refreshPage();
  },
})