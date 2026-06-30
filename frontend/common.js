// solved.ac/problems/tags 기준 (문제 수 내림차순)
const TAG_KO = {
  // page 1
  math:                           '수학',
  implementation:                 '구현',
  dp:                             '다이나믹 프로그래밍',
  data_structures:                '자료 구조',
  graphs:                         '그래프 이론',
  greedy:                         '그리디 알고리즘',
  string:                         '문자열',
  bruteforcing:                   '브루트포스 알고리즘',
  graph_traversal:                '그래프 탐색',
  sorting:                        '정렬',
  ad_hoc:                         '애드 혹',
  geometry:                       '기하학',
  trees:                          '트리',
  number_theory:                  '정수론',
  segtree:                        '세그먼트 트리',
  binary_search:                  '이분 탐색',
  set:                            '집합과 맵',
  constructive:                   '해 구성하기',
  prefix_sum:                     '누적 합',
  arithmetic:                     '사칙연산',
  simulation:                     '시뮬레이션',
  combinatorics:                  '조합론',
  bfs:                            '너비 우선 탐색',
  case_work:                      '많은 조건 분기',
  bitmask:                        '비트마스킹',
  shortest_path:                  '최단 경로',
  dfs:                            '깊이 우선 탐색',
  hash_set:                       '해시를 사용한 집합과 맵',
  dijkstra:                       '데이크스트라',
  sweeping:                       '스위핑',
  // page 2
  disjoint_set:                   '분리 집합',
  backtracking:                   '백트래킹',
  dp_tree:                        '트리에서의 다이나믹 프로그래밍',
  priority_queue:                 '우선순위 큐',
  parsing:                        '파싱',
  parametric_search:              '매개 변수 탐색',
  tree_set:                       '트리를 사용한 집합과 맵',
  game_theory:                    '게임 이론',
  divide_and_conquer:             '분할 정복',
  probability:                    '확률론',
  stack:                          '스택',
  two_pointer:                    '두 포인터',
  dp_bitfield:                    '비트필드를 이용한 다이나믹 프로그래밍',
  lazyprop:                       '느리게 갱신되는 세그먼트 트리',
  primality_test:                 '소수 판정',
  flow:                           '최대 유량',
  offline_queries:                '오프라인 쿼리',
  exponentiation_by_squaring:     '분할 정복을 이용한 거듭제곱',
  knapsack:                       '배낭 문제',
  dag:                            '방향 비순환 그래프',
  arbitrary_precision:            '임의 정밀도 / 큰 수 연산',
  coordinate_compression:         '값 / 좌표 압축',
  recursion:                      '재귀',
  euclidean:                      '유클리드 호제법',
  grid_graph:                     '격자 그래프',
  mst:                            '최소 스패닝 트리',
  topological_sorting:            '위상 정렬',
  linear_algebra:                 '선형대수학',
  precomputation:                 '런타임 전의 전처리',
  convex_hull:                    '볼록 껍질',
  // page 3
  sieve:                          '에라토스테네스의 체',
  inclusion_and_exclusion:        '포함 배제의 원리',
  bipartite_matching:             '이분 매칭',
  lca:                            '최소 공통 조상',
  sparse_table:                   '희소 배열',
  traceback:                      '역추적',
  parity:                         '홀짝성',
  hashing:                        '해싱',
  randomization:                  '무작위화',
  modular_multiplicative_inverse: '모듈로 곱셈 역원',
  floyd_warshall:                 '플로이드–워셜',
  scc:                            '강한 연결 요소',
  smaller_to_larger:              '작은 집합에서 큰 집합으로 합치는 테크닉',
  line_intersection:              '선분 교차 판정',
  sqrt_decomposition:             '제곱근 분할법',
  fft:                            '고속 푸리에 변환',
  calculus:                       '미적분학',
  trie:                           '트라이',
  deque:                          '덱',
  prime_factorization:            '소인수분해',
  geometry_3d:                    '3차원 기하학',
  heuristics:                     '휴리스틱',
  ternary_search:                 '삼분 탐색',
  sliding_window:                 '슬라이딩 윈도우',
  euler_tour_technique:           '오일러 경로 테크닉',
  suffix_array:                   '접미사 배열과 LCP 배열',
  cht:                            '볼록 껍질을 이용한 최적화',
  mcmf:                           '최소 비용 최대 유량',
  sprague_grundy:                 '스프라그–그런디 정리',
  difference_array:               '차분 배열 트릭',
  // page 4
  mitm:                           '중간에서 만나기',
  pythagoras:                     '피타고라스 정리',
  lis:                            '가장 긴 증가하는 부분 수열 문제',
  centroid:                       '센트로이드',
  bitset:                         '비트 집합',
  permutation_cycle_decomposition:'순열 사이클 분할',
  kmp:                            'KMP',
  gaussian_elimination:           '가우스 소거법',
  linearity_of_expectation:       '기댓값의 선형성',
  bipartite_graph:                '이분 그래프',
  hld:                            'Heavy-light 분할',
  mfmc:                           '최대 유량 최소 컷 정리',
  polygon_area:                   '다각형의 넓이',
  centroid_decomposition:         '센트로이드 분할',
  physics:                        '물리학',
  eulerian_path:                  '오일러 경로',
  flt:                            '페르마의 소정리',
  '0_1_bfs':                      '0-1 너비 우선 탐색',
  flood_fill:                     '플러드 필',
  articulation:                   '단절점과 단절선',
  '2_sat':                        '2-SAT',
  queue:                          '큐',
  functional_graph:               '함수형 그래프',
  pigeonhole_principle:           '비둘기집 원리',
  tsp:                            '외판원 순회 문제',
  deque_trick:                    '덱을 이용한 구간 최댓값 트릭',
  rerooting:                      '트리에서의 전방향 다이나믹 프로그래밍',
  pst:                            '퍼시스턴트 세그먼트 트리',
  dp_digit:                       '자릿수를 이용한 다이나믹 프로그래밍',
  planar_graph:                   '평면 그래프',
  // page 5
  bcc:                            '이중 연결 요소',
  euler_phi:                      '오일러 피 함수',
  generating_function:            '생성 함수',
  point_in_convex_polygon:        '볼록 다각형 내부의 점 판정',
  crt:                            '중국인의 나머지 정리',
  angle_sorting:                  '각도 정렬',
  harmonic_number:                '조화수',
  linked_list:                    '연결 리스트',
  invariant:                      '불변량 찾기',
  tree_diameter:                  '트리의 지름',
  mo:                             "Mo's",
  maximum_subarray:               '최대 부분 배열 문제',
  cactus:                         '선인장',
  bellman_ford:                   '벨만–포드',
  divide_and_conquer_optimization:'분할 정복을 사용한 최적화',
  extended_euclidean:             '확장 유클리드 호제법',
  splay_tree:                     '스플레이 트리',
  dp_sum_over_subsets:            '부분집합의 합 다이나믹 프로그래밍',
  half_plane_intersection:        '반평면 교집합',
  pbs:                            '병렬 이분 탐색',
  euler_characteristic:           '오일러 지표',
  rotating_calipers:              '회전하는 캘리퍼스',
  regex:                          '정규 표현식',
  multi_segtree:                  '다차원 세그먼트 트리',
  lcs:                            '최장 공통 부분 수열 문제',
  manacher:                       '매내처',
  pollard_rho:                    '폴라드 로',
  slope_trick:                    '함수 개형을 이용한 최적화',
  aho_corasick:                   '아호-코라식',
  miller_rabin:                   '밀러–라빈 소수 판별법',
  // page 6
  dp_deque:                       '덱을 이용한 다이나믹 프로그래밍',
  mobius_inversion:               '뫼비우스 반전 공식',
  tree_isomorphism:               '트리 동형 사상',
  merge_sort_tree:                '머지 소트 트리',
  point_in_non_convex_polygon:    '오목 다각형 내부의 점 판정',
  cartesian_tree:                 '데카르트 트리',
  numerical_analysis:             '수치해석',
  link_cut_tree:                  '링크/컷 트리',
  simulated_annealing:            '담금질 기법',
  rabin_karp:                     '라빈–카프',
  statistics:                     '통계학',
  li_chao_tree:                   '리–차오 트리',
  dp_connection_profile:          '커넥션 프로파일을 이용한 다이나믹 프로그래밍',
  hall:                           '홀의 결혼 정리',
  xor_basis:                      '배타적 논리합 기저',
  alien:                          'Aliens 트릭',
  berlekamp_massey:               '벌리캠프–매시',
  offline_dynamic_connectivity:   '오프라인 동적 연결성 판정',
  z:                              'Z',
  geometric_boolean_operations:   '도형에서의 불 연산',
  tree_compression:               '트리 압축',
  hungarian:                      '헝가리안',
  linear_programming:             '선형 계획법',
  beats:                          '세그먼트 트리 비츠',
  lucas:                          '뤼카 정리',
  duality:                        '쌍대성',
  circulation:                    '서큘레이션',
  voronoi:                        '보로노이 다이어그램',
  polynomial_interpolation:       '다항식 보간법',
  green:                          '그린 정리',
  // page 7
  dual_graph:                     '쌍대 그래프',
  cdq:                            'CDQ 분할 정복',
  bulldozer:                      'Bulldozer 트릭',
  min_enclosing_circle:           '최소 외접원',
  monotone_queue_optimization:    '단조 큐를 이용한 최적화',
  kitamasa:                       '다항식을 이용한 선형점화식 계산',
  discrete_log:                   '이산 로그',
  general_matching:               '일반적인 매칭',
  pick:                           '픽의 정리',
  matroid:                        '매트로이드',
  suffix_tree:                    '접미사 트리',
  geometry_hyper:                 '4차원 이상의 기하학',
  burnside:                       '번사이드 보조정리',
  dominator_tree:                 '도미네이터 트리',
  differential_cryptanalysis:     '차분 공격',
  utf8:                           'UTF-8 입력 처리',
  degree_sequence:                '차수열',
  tree_decomposition:             '트리 분할',
  pisano:                         '피사노 주기',
  top_tree:                       '탑 트리',
  discrete_sqrt:                  '이산 제곱근',
  palindrome_tree:                '회문 트리',
  bidirectional_search:           '양방향 탐색',
  lgv:                            '린드스트롬–게셀–비엔노 보조정리',
  dial:                           '다이얼',
  rope:                           '로프',
  knuth_x:                        '크누스 X',
  dancing_links:                  '춤추는 링크',
  gradient_descent:               '경사 하강법',
  floor_sum:                      '유리 등차수열의 내림 합',
  // page 8
  stable_marriage:                '안정 결혼 문제',
  bayes:                          '베이즈 정리',
  delaunay:                       '델로네 삼각분할',
  kinetic_segtree:                '키네틱 세그먼트 트리',
  knuth:                          '크누스 최적화',
  birthday:                       '생일 문제',
  bitset_lcs:                     '비트 집합을 이용한 최장 공통 부분 수열 최적화',
  multipoint_evaluation:          '다중 대입값 계산',
  hirschberg:                     '히르쉬버그',
  chordal_graph:                  '현 그래프',
  lte:                            '지수승강 보조정리',
  directed_mst:                   '유향 최소 스패닝 트리',
  stoer_wagner:                   '스토어–바그너',
  hackenbush:                     '하켄부시 게임',
  majority_vote:                  '보이어–무어 다수결 투표',
  rb_tree:                        '레드-블랙 트리',
  a_star:                         'A*',
  treewidth:                      '제한된 트리 너비',
  discrete_kth_root:              '이산 k제곱근',
};

// 한국 코딩 테스트 중요도 순 (티어 1→4 → 나머지 가나다순)
const TAG_PRIORITY = [
  // ── Tier 1: 코테 핵심 ──────────────────────────────
  'implementation',         // 구현
  'simulation',             // 시뮬레이션
  'bruteforcing',           // 브루트포스 알고리즘
  'math',                   // 수학
  'greedy',                 // 그리디 알고리즘
  'dp',                     // 다이나믹 프로그래밍
  'bfs',                    // 너비 우선 탐색
  'dfs',                    // 깊이 우선 탐색
  'graph_traversal',        // 그래프 탐색
  'graphs',                 // 그래프 이론

  // ── Tier 2: 필수 자료구조·기법 ────────────────────
  'sorting',                // 정렬
  'binary_search',          // 이분 탐색
  'string',                 // 문자열
  'prefix_sum',             // 누적 합
  'two_pointer',            // 두 포인터
  'backtracking',           // 백트래킹
  'recursion',              // 재귀
  'stack',                  // 스택
  'queue',                  // 큐
  'deque',                  // 덱
  'priority_queue',         // 우선순위 큐
  'data_structures',        // 자료 구조
  'arithmetic',             // 사칙연산
  'case_work',              // 많은 조건 분기
  'sliding_window',         // 슬라이딩 윈도우
  'difference_array',       // 차분 배열 트릭

  // ── Tier 3: 그래프·트리·탐색 심화 ────────────────
  'shortest_path',          // 최단 경로
  'dijkstra',               // 데이크스트라
  'bellman_ford',           // 벨만–포드
  'floyd_warshall',         // 플로이드–워셜
  '0_1_bfs',                // 0-1 너비 우선 탐색
  'trees',                  // 트리
  'mst',                    // 최소 스패닝 트리
  'disjoint_set',           // 분리 집합
  'topological_sorting',    // 위상 정렬
  'lca',                    // 최소 공통 조상
  'scc',                    // 강한 연결 요소
  'dag',                    // 방향 비순환 그래프
  'grid_graph',             // 격자 그래프
  'flood_fill',             // 플러드 필
  'eulerian_path',          // 오일러 경로
  'articulation',           // 단절점과 단절선
  '2_sat',                  // 2-SAT
  'bipartite_graph',        // 이분 그래프
  'bipartite_matching',     // 이분 매칭

  // ── Tier 3: 수학·정수론 ───────────────────────────
  'number_theory',          // 정수론
  'combinatorics',          // 조합론
  'sieve',                  // 에라토스테네스의 체
  'primality_test',         // 소수 판정
  'prime_factorization',    // 소인수분해
  'euclidean',              // 유클리드 호제법
  'extended_euclidean',     // 확장 유클리드 호제법
  'modular_multiplicative_inverse', // 모듈로 곱셈 역원
  'flt',                    // 페르마의 소정리
  'inclusion_and_exclusion',// 포함 배제의 원리
  'exponentiation_by_squaring', // 분할 정복을 이용한 거듭제곱

  // ── Tier 3: 문자열 고급 ──────────────────────────
  'hashing',                // 해싱
  'hash_set',               // 해시를 사용한 집합과 맵
  'kmp',                    // KMP
  'trie',                   // 트라이
  'suffix_array',           // 접미사 배열과 LCP 배열
  'aho_corasick',           // 아호-코라식
  'manacher',               // 매내처
  'rabin_karp',             // 라빈–카프
  'heuristics',             // 휴리스틱

  // ── Tier 3: DP 심화 ──────────────────────────────
  'knapsack',               // 배낭 문제
  'lis',                    // 가장 긴 증가하는 부분 수열 문제
  'lcs',                    // 최장 공통 부분 수열 문제
  'bitmask',                // 비트마스킹
  'dp_bitfield',            // 비트필드를 이용한 다이나믹 프로그래밍
  'dp_tree',                // 트리에서의 다이나믹 프로그래밍
  'dp_digit',               // 자릿수를 이용한 다이나믹 프로그래밍
  'rerooting',              // 트리에서의 전방향 다이나믹 프로그래밍
  'mitm',                   // 중간에서 만나기

  // ── Tier 3: 분할 정복·기타 알고리즘 ─────────────
  'divide_and_conquer',     // 분할 정복
  'parametric_search',      // 매개 변수 탐색
  'ternary_search',         // 삼분 탐색
  'coordinate_compression', // 값 / 좌표 압축
  'segtree',                // 세그먼트 트리
  'lazyprop',               // 느리게 갱신되는 세그먼트 트리
  'sparse_table',           // 희소 배열
  'sqrt_decomposition',     // 제곱근 분할법
  'precomputation',         // 런타임 전의 전처리

  // ── Tier 4: 자료구조·그래프 고급 ─────────────────
  'set',                    // 집합과 맵
  'tree_set',               // 트리를 사용한 집합과 맵
  'game_theory',            // 게임 이론
  'sprague_grundy',         // 스프라그–그런디 정리
  'flow',                   // 최대 유량
  'mcmf',                   // 최소 비용 최대 유량
  'mfmc',                   // 최대 유량 최소 컷 정리
  'convex_hull',            // 볼록 껍질
  'cht',                    // 볼록 껍질을 이용한 최적화
  'ad_hoc',                 // 애드 혹
  'constructive',           // 해 구성하기
  'sweeping',               // 스위핑
  'offline_queries',        // 오프라인 쿼리
  'arbitrary_precision',    // 임의 정밀도 / 큰 수 연산
  'geometry',               // 기하학
];

function sortTags(tags) {
  const rank = Object.fromEntries(TAG_PRIORITY.map((t, i) => [t, i]));
  return [...tags].sort((a, b) => {
    const ra = rank[a] ?? Infinity;
    const rb = rank[b] ?? Infinity;
    if (ra !== rb) return ra - rb;
    return (TAG_KO[a] || a).localeCompare(TAG_KO[b] || b, 'ko');
  });
}

const LV_LABEL = {
  6:'S5',7:'S4',8:'S3',9:'S2',10:'S1',
  11:'G5',12:'G4',13:'G3',14:'G2',15:'G1',
  16:'P5',17:'P4',18:'P3',19:'P2',20:'P1',
};

function tagKo(tag) { return TAG_KO[tag] || tag; }
function lvClass(l) { return l<=10 ? 'lv-silver' : l<=15 ? 'lv-gold' : 'lv-plat'; }
function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
