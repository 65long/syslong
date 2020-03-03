<template>
  <div>
    <!--面包屑导航区与-->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/roles">角色管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!--看卡片试图-->
    <el-card>
      <!--添加角色按钮-->
      <el-row>
        <el-col><el-button type="primary" @click="showAddRoleDialog">添加角色</el-button></el-col>
      </el-row>
      <el-table :data="roleList" border stripe>
        <!--展开列-->
        <el-table-column type="expand">
          <template slot-scope="scope">
            <!--渲染权限-->
            <el-row v-for="(item1, i1) in scope.row.perms" :key="item1.id" :class="['v-center','bd-bottom', i1===0 ? 'bd-top' : '']">
              <!--一级权限-->
              <el-col :span="5">
                <el-tag closable @close="removeRolePermById(item1.id, scope.row, item1.name)">{{item1.name}}</el-tag>
                <i class="el-icon-caret-right"></i>
              </el-col>
              <!--二级权限-->
              <el-col :span="19">
                <!--通过for循环渲染二级权限-->
                <el-row v-for="(item2, i2) in item1.children" :key="item2.id" :class="[i2===0 ? '' : 'bd-top', 'v-center']">
                  <el-col :span="6">
                    <el-tag type="success" closable @close="removeRolePermById(item2.id, scope.row, item2.name)">{{item2.name}}</el-tag>
                    <i class="el-icon-caret-right"></i>
                  </el-col>
                  <!--三级权限-->
                  <el-col :span="18">
                    <el-tag type="warning" v-for="(item3, i3) in item2.children" :key="item3.id" closable
                            @close="removeRolePermById(item3.id, scope.row, item3.name)">
                        {{item3.name}}
                    </el-tag>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
            <!--<pre>{{scope.row}}</pre>-->
          </template>
        </el-table-column>
        <!--索引列-->
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="name" label="角色名称" width="100"></el-table-column>
        <el-table-column prop="desc" label="角色描述" ></el-table-column>
        <el-table-column label="角色操作" width="200">
            <template slot-scope="scope">
              <!--修改，删除，分配权限-->
              <el-button type="primary" circle size="mini" @click="showEditRoleDialog(scope.row)">编辑</el-button>
              <el-button type="danger" circle size="mini" @click="deleteRole(scope.row)">删除</el-button>
              <!--分配权限，el-tooltip为文本提示按钮-->
              <el-tooltip class="item" effect="dark" content="分配权限" placement="top" :enterable="false">
                <el-button type="primary"  circle size="mini" @click="showAddPermsDialog(scope.row)">分配权限</el-button>
              </el-tooltip>
            </template>
        </el-table-column>
      </el-table>

        <!--分页功能-->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.page"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="queryInfo.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="roleTotal">
        </el-pagination>

      <!--分配权限对话框-->
      <el-dialog
        title="分配权限"
        :visible.sync="addPermsDialogVisible"
        width="50%"
        @close="restDefaultKeys"
      >
        <el-tree :data="allPermsList" :props="treeProps" show-checkbox node-key="id" default-expand-all
        :default-checked-keys="defkeys" ref="treeRef">

        </el-tree>
        <span slot="footer" class="dialog-footer">
          <el-button @click="addPermsDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="assignPerms">确 定</el-button>
        </span>
      </el-dialog>

      <!--修改角色对话框-->
      <el-dialog
        title="修改角色详情"
        :visible.sync="editDialogVisible"
        @close="editDialogClose"
        width="50%">
        <!--这是修改主题区-->
        <el-form ref='editRoleForm' :model='editRoleForm' :rules="editRoleRules" label-width='70px'>
            <el-form-item prop="name" label="角色名称">
                <el-input v-model='editRoleForm.name' placeholder='角色名称'>
                </el-input>
            </el-form-item>

            <el-form-item prop="desc" label="角色描述">
                <el-input v-model='editRoleForm.desc' placeholder='角色描述'></el-input>
            </el-form-item>

        </el-form>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitRoleEdit">确 定</el-button>
        </span>
      </el-dialog>

      <!--添加角色对话框-->
      <el-dialog
        title="添加角色"
        :visible.sync="addDialogVisible"
        @close="addDialogClose"
        width="50%">
        <!--这是添加主题区-->
        <el-form ref='addRoleForm' :model='addRoleForm' :rules="addRoleRules" label-width='70px'>
            <el-form-item prop="name" label="角色名称">
                <el-input v-model='addRoleForm.name' placeholder='请输入角色名称'>
                </el-input>
            </el-form-item>

            <el-form-item prop="desc" label="角色描述">
                <el-input v-model='addRoleForm.desc' placeholder='请输入角色描述'></el-input>
            </el-form-item>

        </el-form>
        <!--底部按钮区域-->
        <span slot="footer" class="dialog-footer">
          <el-button @click="addDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitRoleAdd">确 定</el-button>
        </span>
      </el-dialog>

    </el-card>
  </div>
</template>

<script>
    export default {
        name: "Roles",
      data(){
          return {
            roleTotal: 0,
            //查询角色列表分页
            queryInfo: {
              page: 1,
              size: 5,
            },
            roleList: [],
            allPermsList: [],
            // 显示分配权限对话框
            addPermsDialogVisible: false,
            // 树形控件的属性绑定对象，指定展示那些，指定嵌套关系字段
            treeProps: {
              label: 'name',
              children: 'children'
            },
            //默认选中的节点id值
            defkeys: [],
            // 被操作的角色id
            operRoleId: -1,
            //控制显示编辑角色对话框的显示
            editDialogVisible: false,
            // 修改对话框的提交数据
            editRoleForm: {},
            editRoleRules: {
              name: [
                {required: true, message: '请输入角色名称', trigger: 'blur'},
                {min: 2, max: 8, message: '用户名长度在2-15个字符之间', trigger: 'blur'},
              ],
            },
            addRoleForm: {},
            addRoleRules:{
              name: [
                {required: true, message: '请输入角色名称', trigger: 'blur'},
                {min: 2, max: 8, message: '用户名长度在2-15个字符之间', trigger: 'blur'},
              ],
            },
            //控制显示添加角色对话框显示
            addDialogVisible: false,
          }
      },
      methods: {
        showAddRoleDialog(){
          this.addDialogVisible = !this.addDialogVisible;
        },
        submitRoleAdd(){
          // 提交前的预验证
            this.$refs.addRoleForm.validate(valid => {
              if(!valid){
                // 与验证不合法
                this.$message.error('填写信息错误');
                return
              }else{
                //与验证合法
                // 提交角色编辑的数据
                this.$axios.post(`/rbac/roles/`, this.addRoleForm)
                  .then(res => {
                    this.getRoleList();
                    this.showAddRoleDialog();
                    this.$message.success('添加角色成功');
                  })
                  .catch(err => {
                    this.$message.error('添加角色失败')
                  })
              }
            })
        },
        addDialogClose(){
          this.addRoleForm.clear();
          this.$refs.editRoleForm.resetFields();
        },
        deleteRole(role){
          //删除角色
          this.$confirm(`确定删除【${role.name}】这个角色吗？`, '删除角色',
            {confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'})
            .then(() => {
              this.$axios.delete(`/rbac/roles/${role.id}/`)
                .then(res => {
                  this.$message.success(`删除权限成功---${role.name}`)
                  this.getRoleList();
                })
                .catch(err => {
                  this.$message.error(`删除角色失败---${role.name}`)
                })
            })
            .catch(err => {
              this.$message.warning('已经取消删除')
            });
        },
        editDialogClose(){
          //修改角色对话框关闭之后做的动作，重置表单的验证效果
          // 重置提交数据表单
          this.editRoleForm.clear();
          this.$refs.editRoleForm.resetFields();
        },
        submitRoleEdit(){
          // 提交前的预验证
            this.$refs.editRoleForm.validate(valid => {
              if(!valid){
                // 与验证不合法
                this.$message.error('填写信息错误');
                return
              }else{
                //与验证合法
                // 提交角色编辑的数据
                this.$axios.put(`/rbac/roles/${this.operRoleId}/`, this.editRoleForm)
                  .then(res => {
                    // console.log(res.data);
                    this.roleList.forEach(role => {
                      if (role.id === this.operRoleId) {
                        // console.log(role);
                        role.name = res.data.name;
                        role.desc = res.data.desc;
                      }
                    });
                    this.closeEditRoleDialog();
                    this.$message.success('修改角色信息成功');
                  })
                  .catch(err => {
                    this.$message.error('更改角色信息失败')
                  })
              }
            })
        },
        showEditRoleDialog(role){
          // 打开角色编辑对话狂
          this.operRoleId = role.id;
          this.editDialogVisible = true;
        },
        closeEditRoleDialog(){
          // 关闭角色编辑对话狂
          this.editDialogVisible = false;
        },
        handleSizeChange(newSize){
          // 处理每页数量改变
          this.queryInfo.size = newSize;
          this.getRoleList();

        },
        handleCurrentChange(newPage){
          // 处理当前页码改变
          this.queryInfo.page = newPage;
          this.getRoleList();
        },
        getRoleList(){
          // 获取角色列表数据
            this.$axios.get('/rbac/roles/', {params: this.queryInfo})
              .then(res => {
                this.roleList = res.data.data;
                this.roleTotal = res.data.total;
              })
              .catch(err => {
                this.$message.error('获取角色列表错误')
              })
          },
        getPermListToRole(role){
          // # 获取素有权限
          // console.log(role);
          this.$axios.get('/rbac/perms/', {params: {role_id: role.id}})
            .then(res => {
              this.allPermsList = res.data.allperms;
              this.defkeys = res.data.ownperms;
              // console.log(res.data)
            })
            .catch(err => {
              this.$message.error('获取所有权限列表失败')
            })
        },
        removeRolePermById(perm_id, role, name){
          confirmRes = this.$confirm(`删除该角色的【${name}】权限？`, '删除权限',
            {confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'})
            .then(() => {
              var param = {perm_id, role_id: role.id}
              this.$axios.delete('/rbac/perms/', {data: param})
                .then(res => {
                  this.$message.success(`删除权限成功---${name}`)
                  role.perms = res.data
                })
                .catch(err => {
                  this.$message.error(`删除权限失败---${name}`)
                })
            })
            .catch(err => err);
        },
        showAddPermsDialog(role){
          //保存当前操作的id，后续使用
          this.operRoleId = role.id;
          this.getPermListToRole(role);
          this.addPermsDialogVisible = true;
        },
        //重置defaultkeys，使得用户已经拥有的权限清空
        restDefaultKeys(){
          this.defkeys = []
        },
        assignPerms(){
          //为角色分配权限
          const keys = [
            ...this.$refs.treeRef.getCheckedKeys(),
            ...this.$refs.treeRef.getHalfCheckedKeys()
          ];
          this.$axios.post('/rbac/perms/', {role_id: this.operRoleId, perm_id: keys})
            .then(res => {
              this.$message.success('分配权限成功');
              // role.perms = res.data
              this.roleList.forEach(role => {
                  if(role.id===this.operRoleId){
                    role.perms = res.data;
                  }
              });

              this.addPermsDialogVisible = false;

            })
            .catch(err => {
              this.$message.error('分配权限失败')
            })
        }
      },
      created(){
          this.getRoleList()
      },
    }
</script>

<style scoped>
.v-center{
  display: flex;
  align-items: center;
}
</style>
