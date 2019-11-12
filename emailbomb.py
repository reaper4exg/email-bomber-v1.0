<?php
use Document\Admin\Admin;

class ModelAdminAdmin extends Model {
	/**
	 * Create new Admin
	 * @author: RE70-DECEMBER
	 * @param: 
	 * 	array Data{
	 * 		string Username
	 * 		string Password
	 * 		Object MongoId or string MongoId Group ID
	 * 	}
	 * @return: boolean
	 */
	public function addAdmin( $data = array() ) {
		// Username is required
		if ( !isset($data['username']) || empty($data['username']) ){
			return false;
		}
		
		// Password is required
		if ( !isset($data['password']) || empty($data['password']) ){
			return false;
		}
		
		// Group is required
		if ( !isset($data['group']) ){
			return false;
		}

		$group = $this->dm->getRepository('Document\Admin\Group')->find( $data['group'] );
		if ( !$group ){
			return false;
		}
		
		// Create Admin
		$salt = substr(md5(uniqid(rand(), true)), 0, 9);
		$admin = new Admin();
		$admin->setUsername( $data['username'] );
		$admin->setSalt( $salt );
		$admin->setPassword( sha1($salt . sha1($salt . sha1($data['password']))) );
		$admin->setGroup( $group );
		
		// Add status
		if ( isset($data['status']) ){
			$admin->setStatus( $data['status'] );
		}
		
		// Save to DB
		$this->dm->persist( $admin );
		$this->dm->flush();
		
		return true;
	}

	/**
	 * Edit Admin
	 * @author: RE70-DECEMBER
	 * @param:
	 * 	Admin ID 
	 * 	array Data{
	 * 		string Username
	 * 		string Password
	 * 		Object MongoId or string MongoId Group ID
	 * 	}
	 * @return: boolean
	 */
	public function editAdmin( $id, $data = array() ) {
		// Username is required
		if ( !isset($data['username']) || empty($data['username']) ){
			return false;
		}
		
		// Group is required
		if ( !isset($data['group']) ){
			return false;
		}
		
		$group = $this->dm->getRepository('Document\Admin\Group')->find( $data['group'] );
		if ( !$group ){
			return false;
		}

		$admin = $this->dm->getRepository('Document\Admin\Admin')->find( $id );
		if ( !$admin ){
			return false;
		}
		
		// Update Admin
		if ( isset($data['password']) || !empty($data['password']) ){
			$salt = substr(md5(uniqid(rand(), true)), 0, 9);
			$admin->setSalt( $salt );
			$admin->setPassword( sha1($salt . sha1($salt . sha1($data['password']))) );
		}
		$admin->setUsername( $data['username'] );
		$admin->setGroup( $group );
		
		// Set Status
		if ( isset($data['status']) ){
			$admin->setstatus( $data['status'] );
		}

		$this->dm->flush();
	}

	/**
	 * Delete Admin
	 * @author: RE70-DECEMBER
	 * @param:
	 * 	array Data{
	 * 		int Admin ID
	 * 	}
	 * @return: void
	 */
	public function deleteAdmin( $data = array() ) {
		if ( isset($data['id']) ) {
			foreach ( $data['id'] as $id ) {
				$admin = $this->dm->getRepository( 'Document\Admin\Admin' )->find( $id );
				$this->dm->remove($admin);
			}
		}
		$this->dm->flush();
	}
	
	/**
	 * Get One Admin
	 * @author: RE70-DECEMBER
	 * @param: Admin ID 
	 * @return: Object Admin
	 */
	public function getAdmin( $data = array() ) {
		$admin_repository = $this->dm->getRepository( 'Document\Admin\Admin' );
		
		if ( isset( $data['admin_id']) ){
			return $admin_repository->find( $data['admin_id'] );
		}
		
		if ( isset( $data['email']) ){
			return $admin_repository->findOneBy( array('emails.email' => $data['email']) );
		}
		
		return null;
	}

	/**
	 * Edit List Admins
	 * @author: RE70-DECEMBER
	 * @param:
	 * 	array Data{
	 * 		int Limit
	 * 		int Start
	 * 		int Group ID
	 * 	}
	 * @return: array Object Admins
	 */
	public function getAdmins( $data = array() ) {
		if ( isset($data['group_id']) ){
			return $this->dm->getRepository( 'Document\Admin\Admin' )->findBy( array('group.id' => $data['group_id']) );
		}
		
		if (!isset($data['limit']) || ((int)$data['limit'] < 0)) {
			$data['limit'] = 10;
		}
		
		if (!isset($data['start']) || ((int)$data['start'] < 0)) {
			$data['start'] = 0;
		}

		return $this->dm->getRepository( 'Document\Admin\Admin' )->findAll()->limit( $data['limit'] )->skip( $data['start'] );
	}
	
	/**
	 * Count Total Admins
	 * @author: RE70-DECEMBER
	 * @param: empty
	 * @return: int Total Admin
	 */
	public function getTotalAdmins() {
		$admins = $this->dm->getRepository( 'Document\Admin\Admin' )->findAll();
		return count($admins);
	}
	
	/**
	 * Check Exist Username
	 * @author: RE70-DECEMBER
	 * @param: 
	 *		Object MongoId or string with format MongoId
	 *		string username
	 * @return: boolean
	 */
	public function isExistUsername( $curr_admin_id, $username ) {
		$admins = $this->dm->getRepository( 'Document\Admin\Admin' )->findByUsername( strtolower(trim($username)) );
		
		foreach ( $admins as $admin ) {
			if ( $admin->getId() == $curr_admin_id ){
				continue;
			}

			return true;
		}
		
		return false;
	}
}
?>
