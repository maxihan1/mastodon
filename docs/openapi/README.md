# Mastodon OpenAPI (QA 시험용)

QA Hub Commander 의 Mastodon API 앱(MTI)에 올리는 API 문서 판이다. Mastodon 은 공식 OpenAPI 를 내지 않는다.

- 바탕: [abraham/mastodon-openapi](https://github.com/abraham/mastodon-openapi) `d2287ca` (MIT, 공식 문서에서 자동 생성, Mastodon 4.7.0 기준)
- 더한 것: 원본 생성기는 `methods/` 맨 윗단만 읽어 관리자 API(`/api/v1/admin/*`, `/api/v2/admin/accounts`)가 통째로 빠져 있었다. 하위 폴더도 읽도록 고쳐(`tools/read-admin-folder.patch`) 다시 만들어 **동작 210 → 257개(관리자 47개)**
- 고친 것: 관리자 문서가 공통 이름 `CustomError422` · 예시 둘을 덮어써서 원래대로 되돌리고, 관리자 쪽은 `AdminDomainBlockConflict422` · `AdminTrendsLink200Example` 로 따로 이름 지었다(`tools/fixup.py`)
- 검증: 관리자 경로를 빼면 원본과 동작 · components 가 같다. `redocly lint` 통과(경고만)

다시 만들기: 원본 저장소를 받아 패치를 적용하고 `npm ci && npm run generate` → 원본 `dist/schema.json` 을 `schema.orig.json`, 새 결과를 `mo/dist/schema.json` 자리에 두고 `python3 tools/fixup.py`.

자동 생성이라 실제 서버 응답과 다른 곳이 있을 수 있다. 응답 형식 검사가 실패하면 버그인지 문서 오류인지 사람이 판정한다.
