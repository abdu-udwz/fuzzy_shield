import { useAPI } from "./api";


export function getCollections() {
  return useAPI('collections/').json<string[]>().get()
}
