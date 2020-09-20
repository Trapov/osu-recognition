const UserCard = {
    name: 'UserCard',
    template: `
    <v-card :class="{
      'admin-highlight': isAdmin
    }" :loading="loading">
      <v-dialog
        fullscreen
        v-model="nearestDialog"
      >
        <v-card style="overflow-x:hidden" :loading="loading">
        
          <v-card-actions>
            <v-container fluid>
              <v-row align="center" justify="center">
                <v-col cols="10">
                <v-text-field v-model="nearestSearch" clearable counter prepend-icon="search">
                </v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-actions>

          <v-card-text>
            <v-container fluid>
              <v-list dense>
              <v-row align="center" justify="center" v-for="nearest_user in computedNearest" :key="nearest_user.user_id" >
                <v-col cols="12">
                  <v-list-group no-action ripple two-line prepend-icon="" sub-group>
                    <template v-slot:activator>
                        <v-row align="center" justify="space-around">
                          <v-list-item-content>
                            <v-list-item-title> 
                              {{ (Math.floor((1 - nearest_user.distance) * 100)) + ' %' }}
                            </v-list-item-title>
                            <v-list-item-subtitle style="color:rgb(153,153,0)">
                              [{{nearest_user.user_id}}]
                            </v-list-item-subtitle>
                          </v-list-item-content>

                          <v-btn @click.stop="link(nearest_user.user_id)" small dense>
                            <v-icon>
                              link
                            </v-icon> 
                          </v-btn>

                        </v-row>
                    </template>
                    <v-list-group value="" no-action ripple two-line prepend-icon="" sub-group v-for="feature in nearest_user.features" :key="feature.feature_id_from">
                      <template v-slot:activator>
                      <v-row>
                        <v-list-item-avatar size="55">
                          <v-img
                            :src="toFeatureUrl(item.id, feature.feature_id_from)"
                          >
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title v-text="(Math.floor((1 - feature.distance) * 100)) + ' %'"></v-list-item-title>

                          <v-list-item-subtitle>
                            This feature similar to {{ feature.features_to.length }} other feature(s)
                          </v-list-item-subtitle>
                        </v-list-item-content>

                      </v-row>
                      </template>

                      <v-container fluid>
                      <v-list-item dense v-for="feature_to in feature.features_to" :key="feature_to.feature_id_to"> 
                      <v-row>
                        <v-list-item-avatar size="55">
                          <v-img
                            :src="toFeatureUrl(nearest_user.user_id, feature_to.feature_id_to)"
                          >
                        </v-list-item-avatar> 
                        <v-list-item-content>
                          <v-list-item-title v-text="(Math.floor((1 - feature_to.distance) * 100)) + ' %'"></v-list-item-title>
                          <v-list-item-subtitle v-text="feature_to.feature_id_to.split('.')[0]"></v-list-item-subtitle>
                        </v-list-item-content>
                        
                          <v-btn @click.stop="link_feature(nearest_user.user_id, feature_to.feature_id_to.split('.')[0])" small dense>
                            <v-icon>
                              link
                            </v-icon> 
                          </v-btn>
                          
                        </v-row>
                      </v-list-item>
                      </v-container>

                    </v-list-group>
                  </v-list-group>
                </v-col>
                </v-row>
              </v-list>
            </v-container>
          </v-card-text>
    

          <v-card-actions>
            <v-container fluid>
              <v-row align="center" justify="center">

                <v-btn @click="recalculate" text>
                  <span> Recalculate
                    <v-icon>
                      calculate
                    </v-icon> 
                  </span>
                </v-btn>

                <v-btn text @click="nearestDialog = !nearestDialog">
                  <span>
                    Cancel
                  <v-icon>
                    cancel
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
          left
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
      <v-card-actions>
        <v-btn v-if="item.features.values.length > 1"
          @click="deleteFeature"
          block
          text
          color="red"
        >
          Delete feature
        </v-btn>
      </v-card-actions>
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
      <v-card-actions>
        <v-btn @click="deleteUser()" color="red"  block>
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
    `,
    data() {
      return {
        loading: false,
        userToken: '',
        nearest: [],
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
        return this.nearest.filter(s => {
          return s.user_id.includes(this.nearestSearch) 
        });
      },
      isAdmin: function() {
        return this.item.grants.includes("admin");
      }
    },
    methods: {
      async link_feature(user_id, feature_id) {
        const user_id_to = this.item.id

        console.warn("LINKING ", user_id, user_id_to)

        try {
          this.loading = true;
          const result = await fetch(`/users/link/feature`, {
            method: 'PATCH',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            },
            body: JSON.stringify({
              'user_id': user_id,
              'feature_id': feature_id,
              'user_id_to': user_id_to
            })
          });

          await this.getNearest();

        }
        finally{
          this.loading = false;
        }
      },
      async link(user_id) {
        const user_id_to = this.item.id

        console.warn("LINKING ", user_id, user_id_to)

        try {
          this.loading = true;
          const result = await fetch(`/users/link`, {
            method: 'PATCH',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            },
            body: JSON.stringify({
              'user_id': user_id,
              'user_id_to': user_id_to
            })
          });

          await this.getNearest();

        }
        finally{
          this.loading = false;
        }
      },
      async deleteFeature() {
        try{
          this.loading = true;
          const result = await fetch(`/users/${this.item.id}/features/${this.item.features.values[this.currentImageIndex].feature_id}`, {
            method: 'DELETE',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            }
          });

          if (result.status == 200)
          {
            this.item.features.values.splice(this.currentImageIndex, 1);
          }
        }
        catch(exception){
          console.error(exception)
        }
        finally{
          this.loading = false;

        }
      },
      async deleteUser() {
        try{
          this.loading = true;
          const result = await fetch(`/users/${this.item.id}`, {
            method: 'DELETE',
            headers: {
              'Content-Type' : 'application/json',
              'Authorization': `Bearer ${this.adminToken}`
            }
          });

          if (result.status == 200)
          {
            this.$emit("deleted", this.item.id);
          }
        }
        catch(exception){
          console.error(exception)
        }
        finally{
          this.loading = false;

        }
      },
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

          const theJson = await result.json();
          this.nearest = theJson;
        }
        finally{
          this.loading = false;
        }
      },
      async showNearest() {
        if (this.nearest.length == 0) {
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
        if (this.item.features.values[this.currentImageIndex]) {
          return `/users/${this.item.id}/${this.item.features.values[this.currentImageIndex].image_name}`
        }

        return ""
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