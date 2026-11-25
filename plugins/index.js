/**
 * ECC Plugins for OpenCode (v2)
 *
 * OpenCode 2.0+ loads v2 plugins: the module's default export must be an
 * object `{ id, setup }`. The legacy ECC plugin (`ecc-hooks.ts`) used the v1
 * shape (`{ id, server }`) and is intentionally not loaded here.
 *
 * setup(ctx) registers a few safe hooks:
 *   - tool hook: auto-approve read-only tools (read/glob/grep/search/list)
 *   - tool hook: auto-approve known formatters and test commands
 * Everything else is left to the normal permission flow.
 */

export default {
  id: "ecc-plugins",
  setup: async (ctx) => {
    const tool = ctx && ctx.tool
    if (!tool || typeof tool.hook !== "function") return

    await tool.hook("execute.before", (event) => {
      try {
        const name = event && event.tool
        if (
          ["read", "glob", "grep", "search", "list"].includes(name)
        ) {
          return { approved: true, reason: "Read-only operation" }
        }

        if (name === "shell") {
          let cmd = ""
          const args = event && event.args
          if (typeof args === "string") cmd = args
          else if (args && typeof args === "object" && typeof args.command === "string") cmd = args.command

          if (/^(npx )?(@biomejs\/biome|prettier|black|gofmt|rustfmt|swift-format)/.test(cmd)) {
            return { approved: true, reason: "Formatter execution" }
          }
          if (/^(npm test|npx vitest|npx jest|pytest|go test|cargo test)/.test(cmd)) {
            return { approved: true, reason: "Test execution" }
          }
        }

        return { approved: undefined }
      } catch {
        return { approved: false, reason: "Error in ECC permission hook" }
      }
    })
  },
}
