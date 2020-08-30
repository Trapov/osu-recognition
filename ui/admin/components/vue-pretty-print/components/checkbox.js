
  export default {
    template:
    `  <label
    :class="[ 'vjs-checkbox', value ? 'is-checked': '' ]"
    @click.stop
  >
    <span class="vjs-checkbox__inner" />
    <input
      v-model="model"
      class="vjs-checkbox__original"
      type="checkbox"
      @change="$emit('change', model)"
      @focus="focus = true"
      @blur="focus = false"
    >
  </label>`,
    props: {
      value: {
        type: Boolean,
        default: false
      }
    },
    data () {
      return {
        focus: false
      }
    },
    computed: {
      model: {
        get () {
          return this.value
        },
        set (val) {
          this.$emit('input', val)
        }
      }
    }
  }
