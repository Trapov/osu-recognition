const UserCard = {
    name: 'UserCard',
    template: `
    <v-card :class="{
      'admin-highlight': isAdmin
    }" :loading="loading">
      <v-dialog
        v-model="nearestDialog"
      >
      <v-card :loading="loading" flat>
      <v-card-actions>
        <v-container fluid>
        <v-row align="center" justify="center">
          <v-col cols="8">
            <v-text-field v-model="nearestSearch" clearable counter prepend-icon="search">
            </v-text-field>
          </v-col>
        </v-row>
        </v-container>
      </v-card-actions>
      <v-card-text>
        <v-list>
          <v-list-group prepend-icon="" sub-group v-for="(users, user_id) in computedNearest" :key="user_id">
            <template v-slot:activator>
              <v-list-item-content>
               <span> Near user <span style="color:rgb(153,153,0)"> [{{user_id}}] </span> </span>
              </v-list-item-content>
            </template>

            <v-list-group prepend-icon="" sub-group v-for="(user_features, feature_id_from) in users" :key="feature_id_from">
              <template v-slot:activator>
              <v-list-item-avatar size="60">
              <v-img
                :src="toFeatureUrl(item.id, feature_id_from)"
              >
            </v-list-item-avatar>
                <v-list-item-subtitle>
                  This feature similar to {{ Object.getOwnPropertyNames(user_features).length - 1 }} other feature(s)
                </v-list-item-subtitle>

              </template>

              <v-list-item v-for="(distance, feature_id_to) in user_features" :key="feature_id_to"> 

                <v-list-item-avatar size="55">
                  <v-img
                    :src="toFeatureUrl(user_id, feature_id_to)"
                  >
                </v-list-item-avatar> 
                <v-list-item-content>
                  <v-list-item-title v-text="(Math.floor((1 - distance) * 100)) + ' %'"></v-list-item-title>
                  <v-list-item-subtitle v-text="feature_id_to"></v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>

          </v-list-group>

        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-container fluid>
          <v-row align="center" justify="center">
            <v-btn @click="recalculate" block text large>
              <span> Recalculate
                <v-icon>
                  calculate
                </v-icon> 
              </span>
            </v-btn>
          </v-row>
        </v-container>
      </v-card-actions>
      </v-card>
      </v-dialog>

      <div>
      <v-card-text v-if="showUserToken">
        <v-btn
          @click="showToken()"
          top
          dark
          left
          absolute
        >
          <v-icon>mdi-lastpass</v-icon>
        </v-btn>
        <div class="text-h6" v-html="this.userTokenStyle"> </div>
      </v-card-text>
      <v-img v-else :src="toUrl()"       
        class="white--text align-end"
        height="200px">
        <v-btn
          @click="showToken()"
          top
          absolute
        >
          <v-icon>mdi-lastpass</v-icon>
        </v-btn>
          <v-btn
          @click="showNearest()"
          top
          right
          small
          absolute
        >
          Nearest
        </v-btn>
        <v-btn
          v-if="canGoForward()"
          @click="goForward()"
          fab
          small
          absolute
          center
          right
        >
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
        <v-btn
          v-if="canGoBack()"
          @click="goBack()"
          fab
          small
          absolute
          center
          left
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-card-title>
          {{item.id}}
        </v-card-title>
      </v-img>
      </div>
      <v-card-text>
        <v-text-field readonly append-icon="date_range" v-model="item.created_at">
        </v-text-field>
        <v-text-field readonly append-icon="face" v-model="item.features.count">
        </v-text-field>
        <v-list>
  
          <v-text-field counter v-if="addGrantDialog == item.id" v-model="addGrantModel" append-icon="mdi-check" @click:append="addGrant()">
          </v-text-field>
  
          <v-toolbar  v-else flat>
  
            <v-toolbar-title>
              <span >
                Grants
              </span>
            </v-toolbar-title>
            <v-spacer></v-spacer>
  
            <v-btn @click="addGrantDialog = item.id" icon light>
              <v-icon color="grey darken-2">mdi-plus</v-icon>
            </v-btn>
  
          </v-toolbar>
          <v-list-item @click="" v-for="grant in item.grants" :key="grant">
            <v-list-item-content>
              {{grant}}
            </v-list-item-content>
            <v-list-item-icon>
              <v-btn @click="deleteGrant(grant)" icon color="warn">
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
    `,
    data() {
      return {
        loading: false,
        userToken: '',
        nearest: null,
        showUserToken: false,
        showUserNearest: false,
        nearestSearch: "",
        currentImageIndex: 0,
        addGrantDialog: null,
        addGrantModel: null,
        nearestDialog: false
      }
    },
    computed: {
      userTokenStyle: function() {
        var outString = '';
        var splited = this.userToken.split('.');

        outString += `<span class="red--text">${splited[0]}</span>.`;
        outString += `<span class="purple--text">${splited[1]}</span>.`;
        outString += `<span class="blue--text">${splited[2]}</span>`;
        return outString;
      },
      computedNearest: function() {
        if (!this.nearestSearch) {
          return this.nearest;
        }
        return Object.keys(this.nearest)
        .filter(key => key.includes(this.nearestSearch))
        .reduce((obj, key) => {
          obj[key] = this.nearest[key];
          return obj;
        }, {});
      },
      isAdmin: function() {
        return this.item.grants.includes("admin");
      }
    },
    methods: {
      async recalculate() {
        await this.getNearest()
      },
      async getNearest() {
        try {
          this.loading = true;
          const result = await fetch(`/users/${this.item.id}/nearest`, {
            method: 'GET',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            }
          });

          const theJson = await result.json()
          this.nearest = theJson;
        }
        finally{
          this.loading = false;
        }
      },
      async showNearest() {
        if (this.nearest == null) {
          await this.getNearest();
        }

        this.showUserNearest = !this.showUserNearest;
        this.nearestDialog = !this.nearestDialog;
      },
      async showToken(){

        if (this.showUserToken == true) {
          this.showUserToken = false;
          return;
        }

        if (this.userToken != ''){
          this.showUserToken = true;
          return;
        }

        try {
          this.loading = true;
          const result = await fetch(`/tokens`, {
            method: 'POST',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            },
            body: JSON.stringify({
              'user_id': this.item.id,
            })
          });

          const theJson = await result.json()
          this.userToken = theJson.token;
          this.showUserToken = true;
        }
        finally{
          this.loading = false;
        }
      },
      toFeatureUrl(user_id, image_name) {
        return `/users/${user_id}/${image_name}`
      },
      toUrl() {
        return `/users/${this.item.id}/${this.item.features.values[this.currentImageIndex].image_name}`
      },
      canGoBack() {
        return this.currentImageIndex != 0;
      },
      canGoForward() { 
        return this.currentImageIndex < (this.item.features.count - 1);
      },
      goBack(){
        if(this.canGoBack()){
          this.currentImageIndex -= 1;
        }
      },
      goForward(){
        if (this.canGoForward()){
          this.currentImageIndex += 1;
        }
      },
      async addGrant(){
        try{
          if(this.addGrantModel == '' || this.addGrantModel == null){
            return;
          }
          this.loading = true;
          const result = await fetch(`/grants`, {
            method: 'POST',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            },
            body: JSON.stringify({
              'user_id': this.item.id,
              'grant': this.addGrantModel
            })
          });
          this.item.grants.push(this.addGrantModel);
        }
        catch(exception){
          console.error(exception)
        }
        finally{
          this.addGrantDialog = null;
          this.addGrantModel = null;
          this.loading = false;
        }
      },
  
      async deleteGrant(grant){
        try{
          this.loading = true;
          const result = await fetch(`/grants`, {
            method: 'DELETE',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            },
            body: JSON.stringify({
              'user_id': this.item.id,
              'grant': grant
            })
          });
          this.item.grants = this.item.grants.filter(ug => ug !== grant);
        }
        catch(exception){
          console.error(exception)
        }
        finally{
          this.loading = false;
        }
      }    
    },
    props: [
      'item',
      'adminToken'
    ]
}

export default UserCard;