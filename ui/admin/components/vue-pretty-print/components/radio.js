
  export default {
    template: 
    `
    <label
    :class="[ 'vjs-radio', model === currentPath ? 'is-checked': '' ]"
    @click.stop
  >
    <span class="vjs-radio__inner" />
    <input
      v-model="model"
      class="vjs-radio__original"
      type="radio"
      :value="currentPath"
      @change="change"
      @focus="focus = true"
      @blur="focus = false"
    >
  </label>
    `,
    props: {
      path: {
        type: String,
        default: ''
      },
      value: {
        type: String,
        default: ''
      }
    },
    data () {
      return {
        focus: false
      }
    },
    computed: {
      currentPath () {
        return this.path
      },

      model: {
        get () {
          return this.value
        },
        set (val) {
          this.$emit('input', val)
        }
      }
    },
    methods: {
      change () {
        this.$emit('change', this.model)
      }
    }
  }
