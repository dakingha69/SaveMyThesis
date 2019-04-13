export const secToMs = (version) => {
  return {
    ...version,
    timestamp: version.timestamp * 1000
  }
}