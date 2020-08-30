
  import bracketsMixin from '../mixins/brackets-mixin.js'

  export default {
    mixins: [bracketsMixin],
    template:
    `
    <div>
    <slot />

    <!-- Expand -->
    <span
      v-show="dataVisiable"
      :class="$vuetify.theme.dark ? 'vjs-tree__brackets__dark' : 'vjs-tree__brackets__white'"
      @click.stop="toggleBrackets"
    >
      {{ Array.isArray(data) ? '[' : '{' }}
    </span>

    <!-- Collapse -->
    <span v-show="!dataVisiable">
      <span
        :class="$vuetify.theme.dark ? 'vjs-tree__brackets__dark' : 'vjs-tree__brackets__white'"
        @click.stop="toggleBrackets"
      >
        {{ closedBracketsGenerator(data) }}
      </span>

      <span
        v-if="showLength"
        class="vjs-comment"
      >
        {{ lengthGenerator(data) }}
      </span>
    </span>
  </div>
    `,
    props: {
      showLength: Boolean
    },
    methods: {
      // 关闭括号生成器
      closedBracketsGenerator (data) {
        const brackets = Array.isArray(data) ? '[...]' : '{...}'
        return this.bracketsFormatter(brackets)
      },

      // 长度标记生成器
      lengthGenerator (data) {
        // 若展示长度, 形如 [...] // 3 items
        const text = Array.isArray(data)
          ? `${data.length} items`
          : `${Object.keys(data).length} keys`
        return ` // ${text}`
      }
    }
  }