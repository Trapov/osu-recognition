export function getDataType (value) {
  return Object.prototype.toString.call(value).slice(8, -1).toLowerCase()
}
