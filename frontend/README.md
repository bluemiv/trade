# 프로젝트 구조

## .storybook

Storybook is configured via a folder, called .storybook which contains various configuration files.

## public

static 파일들을 포함한다. static 파일의 종류는 아래와 같다.

- `index.html`
- javascript library files
- images
- 기타 다른 assets

## src

프로젝트의 소스 코드를 포함한다.

### src/assets

assets 파일들을 포함한다.

- images
- css & fonts

### src/components

재사용 가능한 컴포넌트를 포함한다.

각 컴포넌트 폴더에는 component, 테스트, 문서 파일을 포함한다. 예를들어,

**Button component**

- Button/Button.tsx
- Button/Button.style.tsx
- Button/Button.test.tsx
- Button/Button.stories.tsx
- Button/index.tsx

### src/constants

constant 파일을 포함한다.

- Regex
- other application generic constant

### src/helpers

재사용 가능한 helper function을 포함한다.

### src/layouts

It contains the layout components
layout is the common top wrapper component usually will contain navbar , sidebar and children components

### src/pages

It contain the page component.
Each component can layout component as top wrapper based on the page structure
Each component exported as default, since lazy loading works with default export

### src/routes

It contain the page routes
Dynamic configuration is best with working with routes
Usually it have an nested array to render the routes

### src/schema

It contain the schema files using the yup
It used with formik for field validation

### src/service

It contain the dynamic http request function using axios
Axios is a promise-based HTTP Client for node.js and the browser
Axios can be used for api request cancellation, featured with request and response interceptors.

### src/store

It contains the redux files like actions, reducers & actionTypes.

#### src/store/actions

It contains the action files. It used to trigger action to update the redux state

#### src/store/reducers

It contains the reducers files, each file will have default export of function and will have various switch cases to update the redux state

#### src/store/actionTypes.tsx

It contains the actionTypes which will be used to configure reducer & actions.

#### src/store/selectors

It contains the selectors functions, refer Reselect for more details

#### src/store/index.tsx

It contain the create store function which returns a store object

### src/styles

It contain the styled components reusable breakpoints file, global styles & theme constant file

### src/App.js

App Component is the main component in React which acts as a container for all other components

### src/config

It contain the config files using the env

### src/index.js

It contain method to render the application into real dom

### src/test.utils.tsx

It contain method to render the jest component file
This function required since we need to add top wrapper component of react-router, redux & styled-components. Without adding this wrapper component, test cases will not run.
