const algorithms = {
  hamming: "Hamming",
  naive: "Naive",
  levenshtein_ratio: "Lev. Ratio",
  levenshtein_sort: "Lev. Set"
}

export default function useAlgorithms(){
  return {
    algorithms
  }
}

export type ScorerAlgorithm = keyof typeof algorithms
export type ScorerAlgorithmProperty = 'score' |  'time' | 'cpu' | 'memory' | 'match'


