export default {
  props: {
    visible: {
      required: true,
      type: Boolean
    },
    data: {
      required: true
    },
    showComma: Boolean,
    collapsedOnClickBrackets: Boolean
  },
  computed: {
    dataVisiable: {
      get () {
        return this.visible
      },
      set (val) {
        if (this.collapsedOnClickBrackets) {
          this.$emit('update:visible', val)
        }
      }
    }
  },
  methods: {
    toggleBrackets () {
      this.dataVisiable = !this.dataVisiable
    },
    bracketsFormatter (brackets) {
      return this.showComma ? `${brackets},` : brackets
    }
  }
}
