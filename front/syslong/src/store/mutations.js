export default {
// 这里定义更改state中定义的数据同步方法
  // 添加tabs
        add_tabs(state, data) {
            this.state.options.push(data);
        },
}
