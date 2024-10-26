using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvaterManager : MonoBehaviour
{
    AudioSource _audioSource;
    Animator _animator;

    [SerializeField] AudioClip _audioClip;

    void Start()
    {
        _audioSource = GetComponent<AudioSource>();
        _animator = GetComponent<Animator>();

        PlayAnimation();
    }

    // ChatGPT���特���e�L�X�g���擾
    public void GetAudioText()
    {
        //_audioClip = () ���
    }

    // ���N�G�X�g���󂯎������, �����ƃA�j���[�V�����̍Đ�
    public void PlayAnimation()
    {
        _audioSource.PlayOneShot(_audioClip);

        // ���ʂ̕��͂Ȃ�


        //// �i�i�i���͂Ȃ�
        //if ()
        //{
        //    _animator.SetBool("Nanana", true);
        //    StartCoroutine(WaitForAudioEnd("Nanana"));
        //}

        //// �X�C�}�������͂Ȃ�
        //if ()
        //{
        //    _animator.SetBool("Suimamen", true);
        //    StartCoroutine(WaitForAudioEnd("Suimamen"));
        //}
    }

    private IEnumerator WaitForAudioEnd(string pram)
    {
        // �������Đ��I������܂őҋ@
        yield return new WaitUntil(() => !_audioSource.isPlaying);

        // �������I�������炱�̊֐����Ă΂��
        _animator.SetBool(pram, false);
    }
}
