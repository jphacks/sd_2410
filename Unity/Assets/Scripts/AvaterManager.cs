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

    // ChatGPTから音声テキストを取得
    public void GetAudioText()
    {
        //_audioClip = () 代入
    }

    // リクエストを受け取ったら, 音声とアニメーションの再生
    public void PlayAnimation()
    {
        _audioSource.PlayOneShot(_audioClip);

        // 普通の文章なら


        //// ナナナ文章なら
        //if ()
        //{
        //    _animator.SetBool("Nanana", true);
        //    StartCoroutine(WaitForAudioEnd("Nanana"));
        //}

        //// スイマメン文章なら
        //if ()
        //{
        //    _animator.SetBool("Suimamen", true);
        //    StartCoroutine(WaitForAudioEnd("Suimamen"));
        //}
    }

    private IEnumerator WaitForAudioEnd(string pram)
    {
        // 音源が再生終了するまで待機
        yield return new WaitUntil(() => !_audioSource.isPlaying);

        // 音源が終了したらこの関数が呼ばれる
        _animator.SetBool(pram, false);
    }
}
