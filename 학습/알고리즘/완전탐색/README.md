# 완전탐색 (Brute Force)

**언제 씀**: 경우의 수가 충분히 적을 때 (순열 N≤10, 조합 N≤20 수준)  
**시간복잡도**: 순열 O(N!), 조합 O(2^N)

---

## 핵심 패턴

```
순열 (순서 O)    → itertools.permutations(arr, r)
조합 (순서 X)    → itertools.combinations(arr, r)
중복 순열        → itertools.product(arr, repeat=r)
부분집합         → combinations 0~N개 반복
```

---

## 추천 문제

### ✅ 푼 문제
- [x] 모의고사 (Lv.1)
- [x] 소수 찾기 (Lv.2) — 순열
- [x] 카펫 (Lv.2) — 브루트포스
- [x] 피로도 (Lv.2) — 순열

### ⬜ 풀어야 할 문제
- [ ] 불량 사용자 (Lv.3)
- [ ] 외벽 점검 (Lv.3)
