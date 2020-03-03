<template>
    <div>
      <!--面包屑导航区与-->
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item><a href="/users">用户管理</a></el-breadcrumb-item>
          <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>
      <!--卡片试图-->
      <el-card>
        <!--搜索与添加区域-->
        <el-row :gutter="20">
          <el-col :span="7">
              <el-input placeholder="请输入内容" v-model="queryInfo.keyword">
                <el-button slot="append" icon="el-icon-search" @click="searchData"></el-button>
              </el-input>
          </el-col>
          <el-col :span="3">
              <el-button type="primary" @click="addUser">新增用户</el-button>
          </el-col>
        </el-row>
        <!--数据表格区域-->
        <el-table
          :data="userList"
          style="width: 100%"
          stripe border>
          <el-table-column type="index"></el-table-column>

          <el-table-column prop="username" label="姓名" width="100"></el-table-column>
          <el-table-column prop="nickname" label="昵称" width="100"></el-table-column>
          <el-table-column prop="role" label="角色" width="100"></el-table-column>
          <el-table-column prop="email" label="邮箱" width="150"></el-table-column>
          <el-table-column prop="mobile" label="手机号" width="150"></el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <!--修改，删除，分配角色-->
              <el-button type="primary" icon="el-icon-edit" :disabled="scope.row.is_superuser"
                         circle size="mini" @click="showEditDialog(scope.row.id)"></el-button>
              <el-button type="danger" icon="el-icon-delete" :disabled="scope.row.is_superuser"
                         circle size="mini" @click="deleteUser(scope.row.id)"></el-button>
              <!--分配角色，el-tooltip为文本提示按钮-->
              <el-tooltip class="item" effect="dark" content="分配角色" placement="top" :enterable="false">
                <el-button type="primary" icon="el-icon-setting" :disabled="scope.row.is_superuser"
                           circle size="mini" @click="showChangeRoleDialog(scope.row)"></el-button>
              </el-tooltip>
            </template>
          </el-table-column>

        </el-table>
        <!--分页功能-->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[5, 10, 20, 50, 100]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-card>

      <!--这是添加用户对话框-->
      <el-dialog
        title="添加用户"
        :visible.sync="addDialogVisible"
        @close="retForm"
        width="50%">
        <!--这是内容主题区-->
        <el-form ref='addUserForm' :model='addUserForm' :rules="addUserRules" label-width='70px'>
            <el-form-item prop="username" label="用户名">
                <el-input v-model='addUserForm.username' placeholder='请输入用户名'>
                </el-input>
            </el-form-item>

            <el-form-item prop="password" label="密码">
                <el-input v-model='addUserForm.password' placeholder='请输入密码' type='password'></el-input>
            </el-form-item>
            <el-form-item prop="email" label="E-mail">
                <el-input v-model='addUserForm.email' placeholder='请输入邮箱'></el-input>
            </el-form-item>
            <el-form-item prop="mobile" label="手机">
                <el-input v-model='addUserForm.mobile' placeholder='请输入手机'></el-input>
            </el-form-item>
        </el-form>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitAdd">确 定</el-button>
        </span>
      </el-dialog>

      <!--修改用户对话框-->
      <el-dialog
        title="修改用户"
        :visible.sync="editDialogVisible"
        @close="editDialogClose"
        width="50%">
        <!--这是修改主题区-->
        <el-form ref='editUserForm' :model='editUserForm' :rules="editUserRules" label-width='70px'>
            <el-form-item label="用户名">
                <el-input v-model='editUserForm.username' placeholder='禁止修改' :disabled="true">
                </el-input>
            </el-form-item>

            <el-form-item prop="password" label="密码">
                <el-input v-model='editUserForm.password' placeholder='请输入密码' type='password'></el-input>
            </el-form-item>

            <el-form-item prop="nickname" label="昵称">
                <el-input v-model='editUserForm.nickname' placeholder='请输入密码'></el-input>
            </el-form-item>
            <el-form-item prop="email" label="Email">
                <el-input v-model='editUserForm.email' placeholder='请输入昵称'></el-input>
            </el-form-item>
            <el-form-item prop="mobile" label="手机">
                <el-input v-model='editUserForm.mobile' placeholder='请输入手机'></el-input>
            </el-form-item>
        </el-form>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitEdit">确 定</el-button>
        </span>
      </el-dialog>

      <!--更换用户角色对话框-->
      <el-dialog
        title="分配/修改角色"
        :visible.sync="changeUserRoleDialogVisible"
        width="50%">
         <el-select v-model="roleSelect" placeholder="请选择" filterable clearable>
            <el-option
              v-for="role in roleList"
              :key="role.id"
              :label="role.name"
              :value="role.id">
            </el-option>
         </el-select>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="changeUserRoleDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitChangeRole">确 定</el-button>
        </span>
      </el-dialog>


    </div>
</template>

<script>
    export default {
        name: "Users",
        data(){
          // 定影校验手机和邮箱
          var checkMobile = (rule, value, callback) => {
            const regMobile = /^1[34578]\d{9}$/
            // 验证手机号
            if(regMobile.test(value)){
              return callback()
            }
            callback('请输入合法的手机号')
          };
          var checkEmail = (rule, value, callback) => {
            const regEmail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            // 验证手机号
            if(regEmail.test(value)){
              return callback()
            }
            callback('请输入正确的邮箱')
          };
          return {
            userList: [],
            roleList: [],
            // 选择的role
            roleSelect: '',
            queryInfo: {
              keyword: '',
              page: 1,
              size: 5,
            },
            total: 0,
            // 控制添加用户对话框的显示与否
            addDialogVisible: false,
            // 控制修改用户对话框的显示与否
            editDialogVisible: false,
            // 控制更换用户角色对话框的显示与否
            changeUserRoleDialogVisible: false,
            // 添加用户的表单
            addUserForm:{
              username: '',
              password: '',
              email: '',
              mobile: '',
            },
            // 添加用户表单的验证规则
            addUserRules: {
              username: [
                {required: true, message: '请输入用户名', trigger: 'blur'},
                {min: 6, max: 20, message: '用户名长度在6-20个字符之间', trigger: 'blur'},
              ],
              password: [
                {required: true, message: '请输入密码', trigger: 'blur'},
                {min: 6, max: 20, message: '密码长度在6-20个字符之间', trigger: 'blur'},
              ],
              email: [
                {required: false, message: '请输入邮箱', trigger: 'blur'},
                {validator: checkEmail, trigger: 'blur'}
              ],
              mobile: [
                {required: false, message: '请输入手机', trigger: 'blur'},
                {validator: checkMobile, trigger: 'blur'}
              ],
            },
            editUserForm: {},
            editUserRules: {
              nickname: [
                {required: false, message: '请输入昵称', trigger: 'blur'},
              ],
              password: [
                {required: true, message: '请输入密码', trigger: 'blur'},
                {min: 6, max: 20, message: '密码长度在6-20个字符之间', trigger: 'blur'},
              ],
              email: [
                {required: false, message: '请输入邮箱', trigger: 'blur'},
                {validator: checkEmail, trigger: 'blur'}
              ],
              mobile: [
                {required: false, message: '请输入手机', trigger: 'blur'},
                {validator: checkMobile, trigger: 'blur'}
              ],
            },
          }
        },
        created(){
          this.getUserList();
        },
        methods:{
          getUserList(){
            // 获取用户列表
            this.$axios.get('rbac/users/', {params: this.queryInfo})
            .then(res => {
              // this.$message.success('12341234');
              this.userList = res.data.data;
              this.total = res.data.total;
            })
            .catch(err => {
              this.$message.error('getUserList'+ err.message)
            })
          },
          // 处理每页数量改变
          handleSizeChange(newSize){
            this.queryInfo.size = newSize;
            this.getUserList();

          },
          // 处理当前页码改变
          handleCurrentChange(newPage){
            this.queryInfo.page = newPage;
            this.getUserList();
          },
          initCondition(){
            //初始化查询条件
            this.queryInfo.page = 1;
            this.queryInfo.size = 5;
          },
          searchData(){
            this.initCondition();
            this.getUserList();
          },
          //显示添加对话框
          addUser(){
            this.addDialogVisible = true;
          },
          // 关闭对话框之前
          retForm(){
            this.$refs.addUserForm.resetFields()
          },
          // 提交新增用户数据
          submitAdd(){
            // 提交前的预验证
            this.$refs.addUserForm.validate(valid => {
              if(!valid){
                // 与验证不合法
                this.$message.error('填写信息错误');
                return
              }else{
                //与验证合法
                this.$axios.post('/rbac/users/', this.addUserForm)
                  .then( res => {
                    this.$message.success('添加用户成功');
                    this.addDialogVisible = false;
                    this.getUserList();
                  })
                  .catch(err => {
                    this.$message.error('添加用户失败')
                  })
              }
            });
          },
          //显示修改对话框
          showEditDialog(id){
            // this.$message.success('id用户' + id);
            this.$axios.get(`/rbac/users/${id}/`)
              .then(res => {
                // console.log(res.data)
                this.editUserForm = res.data;
              })
              .catch(err => {
                this.$message.success('获取用户信息失败');
              });
            this.editDialogVisible = true;
          },
          //提交修改信息
          submitEdit(){
            // 提交前的预验证
            this.$refs.editUserForm.validate(valid => {
              if(!valid){
                // 与验证不合法
                this.$message.error('填写信息有误');
                return
              }else{
                this.$axios.put(`/rbac/users/${this.editUserForm.id}/`, this.editUserForm)
                  .then(res => {
                    // 修改成功关闭对话框
                    this.editDialogVisible = false;
                    this.$message.success('修改用户信息成功');
                    // 修改成功之后刷新
                    this.getUserList()
                  })
                  .catch(err => {
                    this.$message.error('修改用户信息失败');
                  })
              }
            });
          },
          editDialogClose(){
            // 重置修改表单的验证效果
            this.$refs.editUserForm.resetFields()
          },
          // 删除用户
          deleteUser(id){
            this.$confirm("是否删除用户，不可恢复！", '删除用户',
              {confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'})
              .then(() => {
                // 删除用户
                this.$axios.delete(`/rbac/users/${id}/`)
                  .then(res => {
                    this.$message.success('删除成功');
                    //重新查询数据
                    this.initCondition();
                    this.getUserList();
                  })
                  .catch(err => {
                    this.$message.error('删除失败')
                  })
              })
              .catch(err => {
                this.$message.info('删除取消')
              })
          },
          showChangeRoleDialog(user){
            this.operUserId = user.id;
            this.getRoleList();
            // 控制分配角色对话框的开关
            this.changeUserRoleDialogVisible = true;
          },
          submitChangeRole(){
              // this.$message.success('更改角色' + this.roleSelect)
            this.$axios.post('/rbac/role-to-user/', {user_id: this.operUserId, role_id: this.roleSelect})
              .then(res => {
                this.$message.success('分配角色成功');
                this.userList.forEach(user => {
                  if(user.id=== this.operUserId){
                    user.role = res.data.role;
                  }
                });
                this.changeUserRoleDialogVisible = false;

              })
              .catch(err => {
                this.$message.error('分配角色失败')
              })
          },
          getRoleList(){
            this.$axios.get('/rbac/role-to-user/')
              .then(res => {
                this.roleList = res.data;
                this.$message.success('获取角色列表成功')
              })
              .catch(err => {
                this.$message.error('获取角色列表失败')
              })
          },


        }

    }
</script>

<style lang="less" scoped>

</style>
