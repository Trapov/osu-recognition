

  import bracketsMixin from '../mixins/brackets-mixin.js'

  export default {
    template:
    `
    <div v-show="dataVisiable">
    <span
      :class="$vuetify.theme.dark ? 'vjs-tree__brackets__dark' : 'vjs-tree__brackets__white'"
      @click.stop="toggleBrackets"
    >
      {{ bracketsFormatter(Array.isArray(data) ? ']' : '}') }}
    </span>
  </div>
  `,
    mixins: [bracketsMixin]
  }
