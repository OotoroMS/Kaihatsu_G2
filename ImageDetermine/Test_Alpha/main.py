### ���C���v���O���� ###
# DL, ED, PM�̎O�𑖂点�A���ꂼ��̌��ʂ����Ƃɔ��ʂ��s��

# ���C�u�����̃C���|�[�g

# ���W���[���̃C���|�[�g
import Dtrmn_DL # �f�B�[�v���[�j���O
import Dtrmn_ED # �G�b�W���o
import Dtrmn_PM # �p�^�[���}�b�`���O

# �ϐ��ݒ�
SIZE_IMG = [640, 480] # �S�̂Ŏg�p����摜�T�C�Y

'''
Some things to do:
'''

# �K�؂Ȕ͈͂ɐ؂���
def cut_image():
    # �摜��؂��鏈��
    print("cut_image")

# PLC����̐M�����󂯎��
def get_signal():
    # PLC����̐M�����󂯎�鏈��
    print("get_signal")

# �d�ݕt�����[
def weighted_vote():
    # �d�ݕt�����[�̏���
    print("weighted_vote")

# ���C������
def main():
        ### �摜�����J�n ###
        # �J�����摜���擾
        # �K�؂Ȕ͈͂ɐ؂���
        cut_image()  # �摜��؂��鏈��
        # �摜��SIZE_IMG�Ƀ��T�C�Y

        # �f�B�[�v���[�j���O
        
        # �G�b�W���o

        # �p�^�[���}�b�`���O

        # ����
        #���ꂼ��̌��ʂ���A�d�ݕt�����[���s���A����
        weighted_vote()


if __name__ == "__main__":
    while True:
        if get_signal(): # �J�������V�����摜���擾������A��������PLC����M����������摜����
            main()  # ���C������
        else:
            pass    # �������Ȃ�