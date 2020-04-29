const UserCard = {
    name: 'UserCard',
    template: `
    <v-row align="center" justify="center">
    <v-card :loading="loading">
      <v-img :src="toUrl()"       
      class="white--text align-end"
      height="200px">
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
          {{user.id}}
        </v-card-title>
      </v-img>
      <v-card-text>
        <v-text-field readonly append-icon="date_range" v-model="user.created_at">
        </v-text-field>
        <v-text-field readonly append-icon="face" v-model="user.features.count">
        </v-text-field>
        <v-list>
  
          <v-text-field counter v-if="addGrantDialog == user.id" v-model="addGrantModel" append-icon="mdi-check" @click:append="addGrant()">
          </v-text-field>
  
          <v-toolbar  v-else flat>
  
            <v-toolbar-title>
              <span >
                Grants
              </span>
            </v-toolbar-title>
            <v-spacer></v-spacer>
  
            <v-btn @click="addGrantDialog = user.id" icon light>
              <v-icon color="grey darken-2">mdi-plus</v-icon>
            </v-btn>
  
          </v-toolbar>
          <v-list-item @click="" v-for="grant in user.grants" :key="grant">
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
    </v-row>
    `,
    data() {
      return {
        loading: false,
        currentImageIndex: 0,
        addGrantDialog: null,
        addGrantModel: null,
      }
    },
    methods: {
      toUrl(){
        return `/users/${this.user.id}/${this.user.features.values[this.currentImageIndex].image_name}`
      },
      canGoBack() {
        return this.currentImageIndex != 0;
      },
      canGoForward() { 
        return this.currentImageIndex < (this.user.features.count - 1);
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
              'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
              'user_id': this.user.id,
              'grant': this.addGrantModel
            })
          });
          this.user.grants.push(this.addGrantModel);
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
              'Content-Type' : 'application/json'
            },
            body: JSON.stringify({
              'user_id': this.user.id,
              'grant': grant
            })
          });
          this.user.grants = this.user.grants.filter(ug => ug !== grant);
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
      'user'
    ]
}

export default UserCard;