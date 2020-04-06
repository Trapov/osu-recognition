const UserCard = {
    name: 'UserCard',
    template: `
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
          {{item.id}}
        </v-card-title>
      </v-img>
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
        currentImageIndex: 0,
        addGrantDialog: null,
        addGrantModel: null,
      }
    },
    methods: {
      toUrl(){
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
              'Content-Type' : 'application/json'
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
              'Content-Type' : 'application/json'
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
      'item'
    ]
}

export default UserCard;